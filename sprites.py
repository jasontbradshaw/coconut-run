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

  def set_vel(self, v):
    self.vel = vel

  def valid_pos(self, width):
    if too_left(self) or too_right(self):
      return False
    return True

  def too_left(self):
    """Returns True if avatar is too far to the left of screen"""
    if self.rect.left <= 0: return True
    return False
 
  def too_right(self, width):
    """Returns True if avatar is too far to the right of screen"""
    if self.rect.right >= width: return True
    return False

class Block(pygame.sprite.Sprite):
  ground_lvl = 0
  vel = 0

  def __init__(self, surface, initial_position, vel = 0):
    pygame.sprite.Sprite.__init__(self)
    self.image = surface
    self.rect = self.image.get_rect()
    self.rect.topleft = initial_position
    self.vel = vel

  def update(self):
    """moves block down by self.vel pixels"""
    if not on_ground(self):
      self.rect = self.rect.move(0, self.vel)

  def on_ground(self):
    """returns True if block is on the ground"""
    if self.ground_lvl - self.rect.top - self.rect.height == 0:
      return True
    return False


