import pygame

class Avatar(pygame.sprite.Sprite):
    def __init__(self, surface, initial_position, vel = 0,
            lives = 0, points = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.vel = vel
        self.lives = lives
        self.points = points

    def update(self, dir):
        """
        If dir > 0, move avatar right by self.vel pixels.
        If dir < 0, move avatar left.
        """
        
        if dir > 0:
            self.rect = self.rect.move(self.vel, 0)
        else:
            self.rect = self.rect.move(-self.vel, 0)

    def left_pos(self):
        return self.rect.left

    def right_pos(self):
        return self.rect.left + self.rect.width

class Block(pygame.sprite.Sprite):

    def __init__(self, surface, initial_position, vel = 0, ground_lvl = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.vel = vel
        self.ground_lvl = ground_lvl
        self.time_hit_ground = 0
        self.timeout = 5000     # ms after on ground before killed
        self.hit_ground = False
        self.collided = False   # can only collide w/ avatar once

    def update(self):
        """moves block down by self.vel pixels"""
        if not self.on_ground():
            self.rect = self.rect.move(0, self.vel)
        elif not self.hit_ground:   # has hit ground but flag not set
            # start timeout count down before killing sprite
            self.hit_ground = True
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
        

