import sys
import pygame
import random
import math

from sprites import Block
from sprites import Avatar
from game import Level

# GUI window
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    # resources
    resource_folder = 'resources/'
    fonts_folder = 'fonts/'
    
    avatar_file = resource_folder + 'avatar.bmp'
    block_file = resource_folder + 'coconut.bmp'
    
    COLORKEY = 0xFF00FF # transparent color

    # clock, for fps info and timing
    clk = pygame.time.Clock()

    # keyboard delay before key repeats
    pygame.key.set_repeat(10, 0)

    # level
    lvl = Level("Cocoana", "landscape.bmp",
            120, 0.015, 0.0001, 0.75,
            10, 15,
            0, 0, width, height - 40)

    # avatar
    avatar_surf = pygame.image.load(avatar_file).convert()
    avatar_surf.set_colorkey(COLORKEY)
    avatar_rect = avatar_surf.get_rect()
    avatar_speed = 15
    avatar_lives = 3
    avatar = Avatar(avatar_surf, [lvl.right/2, lvl.bottom - avatar_rect.height],
                    0, 0, avatar_speed, avatar_lives, 0)

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

    # menus
    full_screen_image(resource_folder + "main_menu.png")
    game_over = False

    # main loop
    logic_fps = 3
    skip_ticks = 1000 / logic_fps # ticks between logic updates in milliseconds
    max_frameskip = 5 # minimum fps the game will run at before slowing down

    next_logic_tick = pygame.time.get_ticks()
    loops = 0
    delta = 0.0 # used for interpolation when drawing

    while not game_over:

        loops = 0
        while pygame.time.get_ticks() > next_logic_tick and loops < max_frameskip:
            
            ############
            #  LOGIC   #
            ############

            avatar.update()
            
            # input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_LEFT: # do these last!
                        if avatar.left_pos() > lvl.left:
                            avatar.move(180, avatar.speed)
                    elif event.key == pygame.K_RIGHT:
                        if avatar.right_pos() < lvl.right:
                            avatar.move(0, avatar.speed)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        avatar.vel = 0.0

            # block creation
            if random.random() < lvl.blk_freq:
                block_speed = random.uniform(lvl.min_vel, lvl.max_vel)
                blocks.add(Block(block_surf,
                                 [random.randint(lvl.left, lvl.right), lvl.top],
                                 90, block_speed,
                                 block_speed, lvl.bottom))

            # update game state
            avatar.points += 1
            if lvl.blk_freq < lvl.blk_freq_max:
                lvl.blk_freq += lvl.blk_freq_inc

            # update sprites
            for b in blocks:
                b.update()

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

            next_logic_tick += skip_ticks
            loops += 1

        ############
        # DRAWING  #
        ############

        clk.tick()
        fps = clk.get_fps()

        delta = ((1.0 * pygame.time.get_ticks() + skip_ticks - next_logic_tick)
                 / skip_ticks)
        
        # draw sprites w/ delta movement
        screen.blit(lvl.bg_image, lvl.bg_rect)
        
        for b in blocks:
            b.blit_delta(screen, delta)

        avatar.blit_delta(screen, delta)

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

def get_delta_coords(sprite, delta):
    """Calculate and return the delta coordinates of a particular sprite"""
    rad = math.radians(sprite.dir)
    
    new_x = sprite.previous_position[0] + delta * (sprite.vel * math.cos(rad))
    new_y = sprite.previous_position[1] + delta * (sprite.vel * math.sin(rad))
    
    return [new_x, new_y]

if __name__ == "__main__":
    pygame.init()
    sys.exit(main())

