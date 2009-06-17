import pygame
import math

class Object(pygame.sprite.Sprite):
    def __init__(self, surface, init_pos = [0, 0],
                 dir = 0, vel = 0, speed = -1):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos

        self.dir = dir
        self.vel = vel
        self.speed = speed # how fast we want this sprite to move
        
        self.prev_pos = init_pos
        self.cur_pos = self.rect.topleft

    def move(self, dir, vel):
        """
        Move this sprite's rect by a specified amount.
        dir = direction in degrees (right = 0, down = 90, left = 180, up = 270)
        vel = speed in pixels per tick
        """
        self.dir = dir
        self.vel = vel
        rad = math.radians(self.dir)

        self.prev_pos = self.cur_pos
        self.rect.move_ip(self.vel * math.cos(rad), self.vel * math.sin(rad))
        self.cur_pos = self.rect.topleft

    def blit_delta(self, screen, delta):
        """
        Blit your deltified movement onto a surface.
        screen = surface to blit to
        delta = delta value (0.0 <= delta <= 1.0)
        """
        if self.vel != 0.0:
            rad = math.radians(self.dir)
            
            dx = self.prev_pos[0] + delta * (self.vel * math.cos(rad))
            dy = self.prev_pos[1] + delta * (self.vel * math.sin(rad))
            
            screen.blit(self.image, [dx, dy])
        else:
            screen.blit(self.image, self.cur_pos)

    def update(self):
        """
        Your code here!
        """
        pass
    
class Avatar(Object):
    def __init__(self, surface, init_pos = [0, 0], dir = 0, vel = 0, speed = 30,
                 lives = 0, points = 0):
        Object.__init__(self, surface, init_pos, dir, vel, speed)
        
        self.lives = lives
        self.points = points
    
    def left_pos(self):
        return self.rect.left

    def update(self):
        self.vel = 0.0
        self.prev_pos = self.cur_pos
    
    def right_pos(self):
        return self.rect.left + self.rect.width

class Block(Object):

    def __init__(self, surface, init_pos, dir = 0, vel = 0, speed = 0,
                 ground_lvl = 0):
        Object.__init__(self, surface, init_pos, dir, vel, speed)
        
        self.ground_lvl = ground_lvl
        
        self.time_hit_ground = 0
        self.timeout = 5000     # ms spent on ground before being killed
        self.hit_ground = False
        self.collided = False   # can only collide w/ avatar once

    def update(self):
        """
        Perform movement and check if we're on the ground.
        If we're on the ground, stop.
        """        
        if self.on_ground():
            self.vel = 0
            self.time_hit_ground = pygame.time.get_ticks()
        else:
            self.move(self.dir, self.speed)
            
        # kill sprite if timeout done
        if self.hit_ground and \
           pygame.time.get_ticks() - self.time_hit_ground >= self.timeout:
            self.kill()

    def on_ground(self):
        """returns True if block is on the ground and sets a hit_ground flag"""
        if self.ground_lvl - self.rect.top - self.rect.height <= 0:
            self.hit_ground = True
            return True
        return False

    def collidable(self, avatar):
        """
        returns True if block is collidable with avatar.
        Collidable when:
        1) bottom of block is between the top and halfway point of avatar
        2) has not collided before
        """
        if self.rect.bottom >= avatar.rect.top and \
                not self.collided and \
                self.rect.bottom < (avatar.rect.top + avatar.rect.height / 2):
            return True
        return False
        

