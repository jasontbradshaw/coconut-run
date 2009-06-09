import pygame

class Avatar(pygame.sprite.Sprite):
    def __init__(self, surface, initial_position, vel = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.vel = vel

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

    def update(self):
        """moves block down by self.vel pixels"""
        if not self.on_ground():
            self.rect = self.rect.move(0, self.vel)

    def on_ground(self):
        """returns True if block is on the ground"""
        if self.ground_lvl - self.rect.top - self.rect.height == 0:
            return True
        return False


