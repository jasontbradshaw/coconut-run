import sys, pygame
from sprites import Block, Avatar
pygame.init()

bg_file = 'landscape.bmp'
avatar_file = 'avatar.bmp'
block_file = 'ice.bmp'

# window
size = width, height = 640, 480
speed = [2, 2]
rects = []

screen = pygame.display.set_mode(size)

# keyboard
pygame.key.set_repeat(10, 10)

# load and set up background
bg = pygame.image.load(bg_file).convert()
bg_rect = bg.get_rect()
rects.append(bg_rect)

# load and set up avatar
avatar_surf = pygame.image.load(avatar_file).convert()
avatar_surf.set_colorkey(0xFF00FF)
avatar_rect = avatar_surf.get_rect()
avatar_vel = 10
avatar = Avatar(avatar_surf,
    [width/2, height - avatar_rect.height],
    avatar_vel)

# blocks
block_surf = pygame.image.load(block_file).convert()
block_surf.set_colorkey(0xFF00FF)
b1 = Block(block_surf, [100, 100], 2)

while 1:
  # keyboard handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        if not avatar.too_left():
          avatar.update(-1)
      elif event.key == pygame.K_RIGHT:
        if not avatar.too_right(width):
          avatar.update(1)
      elif event.key == pygame.K_ESCAPE:
        sys.exit()

  if not b1.on_ground(height):
    b1.update()

  screen.blit(bg, bg_rect)
  screen.blit(avatar.image, avatar.rect)
  screen.blit(b1.image, b1.rect)
  pygame.display.flip()
  #pygame.time.delay(10)

