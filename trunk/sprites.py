import pygame
import math
import copy
from libcocorun import Expr
from game import StateMachine

DIR_RIGHT = 0
DIR_DOWN = 90
DIR_LEFT = 180
DIR_UP = 270

class Animatable:
    """
    Provides sprites with an animation framework.

    Animatables have different states. Each state has its own animation.
    The list of states is represented by the StateMachine class.

    An animation is also represented by StateMachine. Each state
    in the StateMachine is a frame of the animation, which is a Surface.
    """

    DEFAULT_MSPF = 100  # ms between frames

    def __init__(self, state_machine):
        self.sm = state_machine
        self.frames = [None]*len(self.sm) # user must set frames later
        self.mspf = [Animatable.DEFAULT_MSPF]*len(self.sm) # ms between frame
        self.next_time = pygame.time.get_ticks()

    def set_frames(self, state, frames, mspf=DEFAULT_MSPF):
        if type(frames) != StateMachine:
            raise TypeError("frames is not a StateMachine!")
        if type(state) == int:
            self.frames[state] = frames
            self.mspf[state] = mspf
        else:
            i = self.sm.index(state)
            self.frames[i] = frames
            self.mspf[i] = mspf

    def change(self, s):
        return self.sm.change(s)

    def current(self, number=False):
        return self.sm.current(number)

    def current_frames(self):
        return self.frames[self.sm.current(True)]

    def next(self):
        # move to the next frame of the current state, but only
        # if it is time to do so
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_time:
            # enough time passed since last update
            mspf = self.mspf[self.sm.current(True)] # for current state
            self.next_time += mspf
            return self.current_frames().next()

    def current_surf(self):
        # get current frame (Surface) of current state
        return self.current_frames().current()

class Movable(pygame.sprite.Sprite):
    def __init__(self, surface, image_bottomleft=(0, 0),
            collision_rect=None, collision_bottomleft=(0,0),
            dir=0, vel=0, speed=-1):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = surface
        self.image_rect = self.image.get_rect() 
        self.image_rect.bottomleft = image_bottomleft
        if collision_rect is None:
            # collision rect not specified, just use whole image
            # note that we cannot let "self.rect is self.image_rect"
            # or else move() will update the same rect TWICE
            self.rect = self.image.get_rect()
            self.rect.bottomleft = image_bottomleft
        else:
            self.rect = collision_rect
            self.rect.bottomleft = collision_bottomleft

        self.dir = dir
        self.vel = vel     # velocity of sprite at current logical frame
                           # used for rendering interpolation
        self.speed = speed # how fast we want this sprite to move
        
        # for interpolation
        self.prev_rect = copy.deepcopy(self.image_rect)

    def move(self, dir, vel):
        """
        Move this sprite's rect by a specified amount.
        dir = direction in degrees (right = 0, down = 90, left = 180, up = 270)
        vel = speed in pixels per tick
        """
        self.prev_rect = copy.deepcopy(self.image_rect)

        self.dir = dir
        self.vel = vel

        rad = math.radians(self.dir)
        dx = self.vel * math.cos(rad)
        dy = self.vel * math.sin(rad)
        self.rect.move_ip(dx, dy)
        self.image_rect.move_ip(dx, dy)

    def get_delta(self, delta):
        """
        Calculate your deltified movement onto a Rect.
        screen = surface to blit to
        delta = delta value (0.0 <= delta <= 1.0)
        """
        rad = math.radians(self.dir)
        
        dx = delta * (self.vel * math.cos(rad))
        dy = delta * (self.vel * math.sin(rad))
        left = self.prev_rect.left + dx
        top = self.prev_rect.top + dy

        return pygame.Rect(left, top,
                self.image_rect.width, self.image_rect.height)

    def position(self):
        """
        Returns an (x, y) tuple of the sprite's current bottomleft position.
        """
        return self.image_rect.bottomleft

    def left_pos(self):
        return self.rect.left

    def right_pos(self):
        return self.rect.right

    def update(self):
        """
        Your code here!

        You must save the previous rect as such:
            self.prev_rect = copy.deepcopy(self.image_rect)
        This is because update() might change the sprite's location
        or future locatin (i.e. move from stopping position or stop
        from moving position).
        """
        pass
    
class Avatar(Movable, Animatable):
    def __init__(self, surface, image_bottomleft=(0, 0),
            collision_rect=None, collision_bottomleft=(0, 0),
            dir=0, vel=0, speed=0,
            lives=0, points=0, states=[]):
        Movable.__init__(self, surface, image_bottomleft,
                collision_rect, collision_bottomleft, dir, vel, speed)
        Animatable.__init__(self, states) 
        self.lives = lives
        self.points = points

    def update_image(self):
        self.image = self.current_surf()
        self.next()

    def update(self):
        if self.sm.current() == "still":
            self.vel = 0.0
        elif self.sm.current() == "left":
            self.move(DIR_LEFT, avatar.speed)
        elif self.sm.current() == "right":
            self.move(DIR_RIGHT, avatar.speed)
        elif self.sm.current() == "scratch":

        self.vel = 0.0      # stop delta avatar movement
        self.prev_rect = copy.deepcopy(self.image_rect)
        self.update_image()
    
class Droppable(Movable):

    def __init__(self, surface, image_bottomleft=(0, 0), dir=0, vel=0, speed=0,
                 ground_lvl=0, timeout=-1):
        Movable.__init__(self, surface, image_bottomleft,
                None, image_bottomleft, dir, vel, speed)
        
        self.ground_lvl = ground_lvl
        
        self.timeout = timeout  # ms spent on ground before being killed
                                # -1 = infinity

        self.time_hit_ground = 0
        self.hit_ground = False
        self.collided = False   # can only collide w/ avatar once
        self.touched = False

    def update(self):
        """
        Perform movement and check if we're on the ground.
        If we're on the ground, stop.
        """
        self.prev_rect = self.image_rect
        self.vel = 0.0
        
        if not self.on_ground():
            self.move(self.dir, self.speed)
        elif not self.hit_ground:   # has hit ground but flag not set
            # start timeout count down before killing sprite
            self.hit_ground = True
            self.time_hit_ground = pygame.time.get_ticks()
        else:   # on ground
            self.vel = 0
            
        # kill sprite if timeout done
        if (self.timeout != -1 and self.hit_ground and
           pygame.time.get_ticks() - self.time_hit_ground >= self.timeout):
            self.kill()

    def on_ground(self):
        """returns True if block is on the ground"""
        if self.ground_lvl - self.rect.bottom <= 0:
            return True
        return False

    def actionable(self, avatar):
        """
        Returns True when Droppable and Avatar meet some requirement so that
        an action by the game can be done.

        Requirements are defined by derived classes.
        """
        pass
        
class Coconut(Droppable):
     
    def __init__(self, surface, init_pos, dir = 0, vel = 0, speed = 0,
            ground_lvl = 0, timeout=-1, expr = Expr()):
        Droppable.__init__(self, surface, init_pos, dir, vel, speed,
                ground_lvl, timeout)
        self.expr = expr

    def value(self):
        try:
            return self.expr.eval()
        except:
            return -1

    def actionable(self, avatar):
        """
        Returns True if:
        1) Coconut and Avatar have collided (assumed).
        2) Coconut is touching the top half of Avatar.
        3) Has not collided before.
        """
        if (self.rect.bottom >= avatar.rect.top and not self.collided and
                self.rect.bottom < (avatar.rect.top + avatar.rect.height/2)):
            return True
        return False

class Banana(Droppable):

    def actionable(self, avatar):
        """
        Returns True if:
        1) Banana and Avatar have collided (assumed).
        2) Banana is not on ground.
        3) Has not collided before.
        """
        if not self.on_ground() and not self.collided:
            return True
        return False

