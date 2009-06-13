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
    block_file = resource_folder + 'coconut.bmp'
    COLORKEY = 0xFF00FF # transparent color

    # GUI window
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)

    # clock, for fps info and timing
    clk = pygame.time.Clock()

    # keyboard delay before key repeats
    pygame.key.set_repeat(10, 10)

    # load level
    lvl = Level("Cocoana", "landscape.bmp", 120, -1, 10, 15,
                0, 0, width, height)

    # load and set up avatar
    avatar_surf = pygame.image.load(avatar_file).convert()
    avatar_surf.set_colorkey(COLORKEY)
    avatar_rect = avatar_surf.get_rect()
    avatar_vel = 4
    avatar = Avatar(avatar_surf,
                    [lvl.right/2, lvl.bottom - avatar_rect.height],
                    avatar_vel, 10, 0)

    # blocks
    block_surf = pygame.image.load(block_file).convert()
    block_surf.set_colorkey(COLORKEY)
    blocks = pygame.sprite.Group()
    block_freq = 0.02 # how often we want blocks to fall; chance per frame
    blocks_left = lvl.max_blocks # how many blocks we can still create
    
    # large game font
    default_font = pygame.font.Font("resources/fonts/anmari.ttf", 26)
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    fps_display_pos = (lvl.right - 140, 20)
    level_display_pos = (lvl.right / 2 - 50, 20)
    lives_display_pos = (20, 20)

    while 1:
        # input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if avatar.left_pos() > lvl.left:
                        avatar.update(-1)
                        avatar.image = pygame.transform.flip(avatar.image,
                                                             True, False)
                elif event.key == pygame.K_RIGHT:
                    if avatar.right_pos() < lvl.right:
                        avatar.update(1)
                        avatar.image = pygame.transform.flip(avatar.image,
                                                             True, False)
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
        
        #block creation
        if random.random() < block_freq and blocks_left != 0:
            # we use != instead of > so when lvl.max_blocks < 0,
            # we can create blocks indefinitely
            blocks_left -= 1
            blocks.add(Block(block_surf,
                             [random.randint(lvl.left, lvl.right), lvl.top],
                             random.uniform(lvl.min_vel, lvl.max_vel),
                             lvl.bottom))

        # update sprites
        blocks.update() 

        # calculate state conditions

        # collision detection
        collide_list = pygame.sprite.spritecollide(avatar, blocks, False)
        for c in collide_list:
            if c.collidable(avatar):
                avatar.lives -= 1
                c.collided = True   # each block can only collide once

        # update game state

        # fps
        clk.tick(60) # used by get_fps(), limits framerate (a 'hack' for now)
        fps = clk.get_fps()

        # redraw
        screen.blit(lvl.bg_image, lvl.bg_rect)
        for b in blocks:
            screen.blit(b.image, b.rect)
        screen.blit(avatar.image, avatar.rect)
        screen.blit(default_font.render(lvl.name, 1, COLOR_WHITE),
                level_display_pos)
        screen.blit(default_font.render('FPS: %.f' % fps, 1, COLOR_BLACK),
                fps_display_pos)
        screen.blit(default_font.render('Lives: %d' % avatar.lives, 1, COLOR_BLACK),
                lives_display_pos)
        pygame.display.flip()
        #pygame.time.delay(10)

if __name__ == "__main__":
        sys.exit(main())

