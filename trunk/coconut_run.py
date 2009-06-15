import sys
import pygame
import random

from sprites import Block
from sprites import Avatar
from game import Level

# GUI window
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    resource_folder = 'resources/'
    fonts_folder = 'fonts/'
    avatar_file = resource_folder + 'avatar.bmp'
    block_file = resource_folder + 'coconut.bmp'
    COLORKEY = 0xFF00FF # transparent color

    # clock, for fps info and timing
    clk = pygame.time.Clock()

    # keyboard delay before key repeats
    pygame.key.set_repeat(10, 10)

    # load level
    lvl = Level("Cocoana", "landscape.bmp",
            120, 0.015, 0.00001, 0.1,
            1, 3,
            0, 0, width, height - 40)

    # load and initialize avatar
    avatar_surf = pygame.image.load(avatar_file).convert()
    avatar_surf.set_colorkey(COLORKEY)
    avatar_rect = avatar_surf.get_rect()
    avatar_vel = 8
    avatar = Avatar(avatar_surf,
                    [lvl.right/2, lvl.bottom - avatar_rect.height],
                    avatar_vel, 3, 0)

    # blocks
    block_surf = pygame.image.load(block_file).convert()
    block_surf.set_colorkey(COLORKEY)
    blocks = pygame.sprite.Group()
    
    # text
    default_font = pygame.font.Font(resource_folder + fonts_folder +
                                    "anmari.ttf", 26)
    COLOR_BLACK = (0, 0, 0)
    fps_display_pos = (lvl.right - 140, 20)
    level_display_pos = (lvl.right / 2 - 50, 20)
    lives_display_pos = (20, 20)
    points_display_pos = (20, 50)

    full_screen_image(resource_folder + "main_menu.png")
    game_over = False

    # main loop
    LOGIC_TICKS = 30
    SKIP_TICKS = 1000 / LOGIC_TICKS # used for delta
    MAX_FRAMESKIP = 5 # minimum fps the game will run at before slowing down

    tick_count = pygame.time.get_ticks()
    loops = 0
    delta = 0.0 # used for interpolation when drawing

    while not game_over:

        loops = 0
        while pygame.time.get_ticks() > tick_count and loops < MAX_FRAMESKIP:
            
            ############
            #  LOGIC   #
            ############

            # input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if avatar.left_pos() > lvl.left:
                            avatar.update(-1)
                    elif event.key == pygame.K_RIGHT:
                        if avatar.right_pos() < lvl.right:
                            avatar.update(1)
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit()
            
            # collision detection
            collide_list = pygame.sprite.spritecollide(avatar, blocks, False)
            for c in collide_list:
                if c.collidable(avatar):
                    if avatar.lives > 0:
                        avatar.lives -= 1
                    else:
                        # go to game over screen and quit
                        full_screen_image(resource_folder + "game_over.png")
                        game_over = True
                    c.collided = True   # each block can only collide once

            # block creation
            if random.random() < lvl.blk_freq:
                blocks.add(Block(block_surf,
                                 [random.randint(lvl.left, lvl.right), lvl.top],
                                 random.uniform(lvl.min_vel, lvl.max_vel),
                                 lvl.bottom))

            # update game state
            avatar.points += 1
            if lvl.blk_freq < lvl.blk_freq_max:
                lvl.blk_freq += lvl.blk_freq_inc
                tick_count += SKIP_TICKS
                loops += 1

        ############
        # DRAWING  #
        ############

        clk.tick()
        fps = clk.get_fps()

        delta = (pygame.time.get_ticks() + SKIP_TICKS - tick_count) / SKIP_TICKS
        
        # draw sprites
        screen.blit(lvl.bg_image, lvl.bg_rect)
        for b in blocks:
            screen.blit(b.image, b.rect)
        screen.blit(avatar.image, avatar.rect)

        # draw text
        screen.blit(default_font.render(lvl.name, 1, COLOR_BLACK),
                level_display_pos)
        screen.blit(default_font.render('FPS: %.1f' % fps, 1, COLOR_BLACK),
                                        fps_display_pos)
        screen.blit(default_font.render('Lives: %d' % avatar.lives, 1,
                                        COLOR_BLACK), lives_display_pos)
        screen.blit(default_font.render('Points: %d' % avatar.points, 1,
                                        COLOR_BLACK), points_display_pos)
        # draw debug text
        screen.blit(default_font.render('blk_freq: %f' % lvl.blk_freq, 1,
                                        COLOR_BLACK), (20, 80))
        pygame.display.flip()

        # update sprites
        blocks.update() 
        

def full_screen_image(img_filename):
    menu_surf = pygame.image.load(img_filename).convert()
    menu_rect = menu_surf.get_rect()
    start_game = False
    while not start_game:
        # input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game = True
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
        screen.blit(menu_surf, menu_rect)
        pygame.display.flip()
        clk = pygame.time.Clock()
        clk.tick()

if __name__ == "__main__":
    pygame.init()
    sys.exit(main())

