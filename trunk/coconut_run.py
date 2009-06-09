import sys
import pygame
import random

from sprites import Block
from sprites import Avatar
from game import Game
from game import Level

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
    lvl = Level("Level 1", "landscape.bmp", 120, -1, 1, 3, 0, 0, width, height)

    # load and set up avatar
    avatar_surf = pygame.image.load(avatar_file).convert()
    avatar_surf.set_colorkey(COLORKEY)
    avatar_rect = avatar_surf.get_rect()
    avatar_vel = 4
    avatar = Avatar(avatar_surf,
                    [lvl.right/2, lvl.bottom - avatar_rect.height],
                    avatar_vel)

    # blocks
    block_surf = pygame.image.load(block_file).convert()
    block_surf.set_colorkey(COLORKEY)
    blocks = pygame.sprite.Group()
    
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
        #block creation
        blockFreq = 0.002 # how often we want blocks to fall as chance per frame
        if random.random() < blockFreq:
            blocks.add(Block(block_surf,
                             [random.randint(lvl.left, lvl.right), lvl.top],
                             random.uniform(lvl.min_vel, lvl.max_vel), lvl.top))

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

