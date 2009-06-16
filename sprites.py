import pygame
import math

class Avatar(pygame.sprite.Sprite):
    def __init__(self, surface, initial_position, dir = 0, vel = 0,
                 lives = 0, points = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position

        self.dir = dir
        self.vel = vel
        
        self.lives = lives
        self.points = points

    def update(self, dir = 0, vel = 0):
        """
        dir = direction in degrees (right = 0, down = 90, left = 180, up = 270)
        vel = speed in pixels per tick
        """
        self.dir = dir
        self.vel = vel
        rad = math.radians(self.dir)
        
        self.rect.move_ip(self.vel * math.cos(rad), self.vel * math.sin(rad))
        
    def left_pos(self):
        return self.rect.left

    def right_pos(self):
        return self.rect.left + self.rect.width

class Block(pygame.sprite.Sprite):

    def __init__(self, surface, initial_position, dir = 0, vel = 0,
                 ground_lvl = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        
        self.dir = dir
        self.vel = vel
        
        self.ground_lvl = ground_lvl
        self.time_hit_ground = 0
        self.timeout = 5000     # ms after on ground before killed
        self.hit_ground = False
        self.collided = False   # can only collide w/ avatar once

    def update(self, dir = 0, vel = 0):
        """
        dir = direction in degrees (right = 0, down = 90, left = 180, up = 270)
        vel = speed in pixels per tick
        """
        self.dir = dir
        self.vel = vel
        rad = math.radians(self.dir)
        
        if not self.on_ground():
            self.rect.move_ip(self.vel * math.cos(rad), self.vel * math.sin(rad))
        elif not self.hit_ground:   # has hit ground but flag not set
            # start timeout count down before killing sprite
            self.hit_ground = True
            #self.vel = 0
            self.time_hit_ground = pygame.time.get_ticks()
        
        # kill sprite if timeout done
        if self.hit_ground and \
           pygame.time.get_ticks() - self.time_hit_ground >= self.timeout:
            self.kill()

    def on_ground(self):
        """returns True if block is on the ground"""
        if self.ground_lvl - self.rect.top - self.rect.height <= 0:
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
        

