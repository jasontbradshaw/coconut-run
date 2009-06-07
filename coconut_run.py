import sys, pygame
from sprites import Block, Avatar
pygame.init()

def main(argv=None):
  """ main game loop """
  if argv is None:
    argv = sys.argv

  resource_folder = 'resources/'
  bg_file = resource_folder + 'landscape.bmp'
  avatar_file = resource_folder + 'avatar.bmp'
  block_file = resource_folder + 'ice.bmp'
  COLORKEY = 0xff00ff         # transparent color

  # GUI window
  size = width, height = 640, 480
  screen = pygame.display.set_mode(size)

  # keyboard delay before key repeats
  pygame.key.set_repeat(10, 10)

  # load and set up background
  bg = pygame.image.load(bg_file).convert()
  bg_rect = bg.get_rect()

  # load and set up avatar
  avatar_surf = pygame.image.load(avatar_file).convert()
  avatar_surf.set_colorkey(COLORKEY)
  avatar_rect = avatar_surf.get_rect()
  avatar_vel = 10
  avatar = Avatar(avatar_surf,
      [width/2, height - avatar_rect.height],
      avatar_vel)

  # blocks (currently just testing one block)
  block_surf = pygame.image.load(block_file).convert()
  block_surf.set_colorkey(COLORKEY)
  b1 = Block(block_surf, [100, 100], 2)

  while 1:
    # input handling
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

    # update state
    if not b1.on_ground(height):
      b1.update()

    # calculate state conditions


    # redraw
    screen.blit(bg, bg_rect)
    screen.blit(avatar.image, avatar.rect)
    screen.blit(b1.image, b1.rect)
    pygame.display.flip()
    #pygame.time.delay(10)

if __name__ == "__main__":
    sys.exit(main())

