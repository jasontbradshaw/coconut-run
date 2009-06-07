import pygame

class Avatar(pygame.sprite.Sprite):
  def __init__(self, surface, initial_position, vel = 0):
    pygame.sprite.Sprite.__init__(self)
    self.image = surface
    self.rect = self.image.get_rect()
    self.rect.topleft = initial_position
    self.vel = vel

  def update(self, dir):
    if dir > 0:
      self.rect = self.rect.move(self.vel, 0)
    else:
      self.rect = self.rect.move(-self.vel, 0)

  def set_vel(self, v):
    self.vel = vel

  def valid_pos(self, width):
    if self.rect.left < 0 or self.rect.right > width + self.rect.width:
      return False
    return True

  def too_left(self):
    if self.rect.left <= 0: return True
    return False
 
  def too_right(self, width):
    if self.rect.right >= width: return True
    return False

  def on_ground(self, ground_lvl):
    if ground_lvl - self.rect.top - self.rect.height == 0:
      return True
    return False

class Block(pygame.sprite.Sprite):
  def __init__(self, surface, initial_position, vel = 0):
    pygame.sprite.Sprite.__init__(self)
    self.image = surface
    self.rect = self.image.get_rect()
    self.rect.topleft = initial_position
    self.vel = vel

  def update(self):
    self.rect = self.rect.move(0, self.vel)

  def set_vel(self, v):
    self.vel = vel

  def on_ground(self, ground_lvl):
    if ground_lvl - self.rect.top - self.rect.height == 0:
      return True
    return False
