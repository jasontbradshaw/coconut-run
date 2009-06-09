import sys, pygame
from sprites import Block, Avatar
from game import Game, Level
pygame.init()

def main(argv=None):
    """ main game loop """
    if argv is None:
        argv = sys.argv

    resource_folder = 'resources/'
    avatar_file = resource_folder + 'avatar.bmp'
    block_file = resource_folder + 'ice.bmp'
    COLORKEY = 0xff00ff                 # transparent color

    # GUI window
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)

    # keyboard delay before key repeats
    pygame.key.set_repeat(10, 10)

    # load level
    lvl = Level()

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
    blocks = pygame.sprite.Group()
    # make some test blocks
    blocks.add(Block(block_surf, [100, 0], 2, height))
    blocks.add(Block(block_surf, [400, 0], 4, height))

    while 1:
        # input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if avatar.left_pos() > lvl.left_cutoff:
                        avatar.update(-1)
                elif event.key == pygame.K_RIGHT:
                    if avatar.right_pos() < lvl.right_cutoff:
                        avatar.update(1)
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()

        # update sprites
        blocks.update() 

        # calculate state conditions

        # update game state

        # redraw
        screen.blit(lvl.bg_image, lvl.bg_rect)
        screen.blit(avatar.image, avatar.rect)
        for b in blocks:
            screen.blit(b.image, b.rect)
        pygame.display.flip()
        #pygame.time.delay(10)

if __name__ == "__main__":
        sys.exit(main())

