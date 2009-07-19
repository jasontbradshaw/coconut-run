import pygame
import math
import copy
from libcocorun import Expr
from game import StateMachine

class Animatable:
    """
    list of States, each element in this list maps (via index) to:
    """
    def __init__(self, state_machine):
        self.sm = state_machine
        self.frames = [None]*len(self.sm) # user must set frames later
        self.mspf = 200 # ms per frame
        self.next_time = pygame.time.get_ticks()
    def set_frames(self, state, frames):
        if type(frames) != StateMachine:
            raise TypeError("frames is not a StateMachine!")
        if type(state) == int:
            self.frames[state] = frames
        else:
            self.frames[self.sm.index(state)] = frames
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
            self.next_time += self.mspf
            return self.current_frames().next()
    def current_surf(self):
        # for the current state frames, returns the current Surface
        return self.current_frames().current()

class Movable(pygame.sprite.Sprite):
    def __init__(self, surface, init_pos =(0, 0),
            dir=0, vel=0, speed=-1):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = surface

        self.rect = self.image.get_rect()
        self.rect.bottomleft = init_pos

        self.dir = dir
        self.vel = vel     # velocity of sprite at current logical frame
                           # used for rendering interpolation
        self.speed = speed # how fast we want this sprite to move
        
        self.prev_rect = copy.deepcopy(self.rect)

    def position(self):
        """
        Returns an (x, y) tuple of the sprite's current bottomleft position.
        """
        return self.rect.bottomleft

    def move(self, dir, vel):
        """
        Move this sprite's rect by a specified amount.
        dir = direction in degrees (right = 0, down = 90, left = 180, up = 270)
        vel = speed in pixels per tick
        """
        self.dir = dir
        self.vel = vel
        rad = math.radians(self.dir)

        self.prev_rect = copy.deepcopy(self.rect)
        self.rect.move_ip(self.vel * math.cos(rad), self.vel * math.sin(rad))

    def get_delta(self, delta):
        """
        Calculate your deltified movement onto a surface.
        screen = surface to blit to
        delta = delta value (0.0 <= delta <= 1.0)
        """
        rad = math.radians(self.dir)
        
        dx = delta * (self.vel * math.cos(rad))
        dy = delta * (self.vel * math.sin(rad))
        left = self.prev_rect.left + dx
        top = self.prev_rect.top + dy

        #return self.rect
        return pygame.Rect(left, top, self.rect.width, self.rect.height)

    def update(self):
        """
        Your code here!
        """
        pass
    
class Avatar(Movable, Animatable):
    def __init__(self, surface, init_pos = (0, 0), dir = 0, vel = 0, speed = 30,
            lives = 0, points = 0, states = []):
        Movable.__init__(self, surface, init_pos, dir, vel, speed)
        Animatable.__init__(self, states) 
        self.lives = lives
        self.points = points

    def update_image(self):
        self.image = self.current_surf()
        self.next()

    def update(self):
        self.vel = 0.0
        self.prev_rect = self.rect
        self.update_image()
    
    def left_pos(self):
        return self.rect.left

    def right_pos(self):
        return self.rect.right

class Droppable(Movable):

    def __init__(self, surface, init_pos, dir = 0, vel = 0, speed = 0,
                 ground_lvl = 0, timeout=-1):
        Movable.__init__(self, surface, init_pos, dir, vel, speed)
        
        self.collide_rect = self.rect
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
        self.vel = 0.0
        self.prev_rect = copy.deepcopy(self.rect)
        
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

