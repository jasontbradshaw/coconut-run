import sys
import pygame
import random
import math
import copy

from sprites import Droppable
from sprites import Avatar
from sprites import Coconut
from sprites import Banana
from game import Level
from game import Music
from libcocorun import Expression

# constants
COLORKEY = 0xFF00FF # transparent color
DIR_RIGHT = 0
DIR_DOWN = 90
DIR_LEFT = 180
DIR_UP = 270

DEFAULT_TIMEOUT = 3000

resource_folder = 'resources/'
audio_folder = resource_folder + 'audio/'
graphics_folder = resource_folder + 'graphics/'
avatar_folder = graphics_folder + 'avatar/'
backdrops_folder = graphics_folder + 'backdrops/'
droppable_folder = graphics_folder + 'droppable/'
icons_folder = graphics_folder + 'icons/'
items_folder = graphics_folder + 'items/'
fonts_folder = resource_folder + 'fonts/'

# GUI window
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    # resources
    avatar_file = avatar_folder + 'avatar.png'
    #coconut_file = droppable_folder + 'coconut.png'
    coconut_file = icons_folder + 'coconut_highres.png'
    #banana_file = droppable_folder + 'banana.png'
    banana_file = icons_folder + 'banana_highres.png'

    # clock, for fps info and timing
    clk = pygame.time.Clock()

    # keyboard delay before key repeats
    pygame.key.set_repeat(10, 0)

    # level
    lvl = Level("Cocoana", backdrops_folder + "landscape.png",
            120, 0.015, 0.0001, 0.75,
            10, 15,
            0, 0, width, height - 40)
    expr = Expression()

    bg_music = Music(audio_folder + 'sample_music.ogg')
    bg_music.play()

    # load surfaces
    avatar_surf = pygame.image.load(avatar_file).convert_alpha()
    coconut_surf = pygame.image.load(coconut_file).convert_alpha()
    banana_surf = pygame.image.load(banana_file).convert_alpha() 

    # set up avatar
    avatar_rect = avatar_surf.get_rect()
    avatar_speed = 15
    avatar_lives = 20
    avatar = Avatar(avatar_surf, (0, lvl.bottom),
                    0, 0, avatar_speed, avatar_lives, 0)

    # make groups
    coconuts = pygame.sprite.Group()
    bananas = pygame.sprite.Group()

    # text
    default_font = pygame.font.Font(fonts_folder + "anmari.ttf", 26)
    COLOR_BLACK = (0, 0, 0)
    
    fps_display_pos = (lvl.right - 140, 20)
    level_display_pos = (lvl.right / 2 - 50, 20)
    lives_display_pos = (20, 20)
    points_display_pos = (20, 50)

    # menus
    full_screen_image(backdrops_folder + "main_menu.png")
    game_over = False

    # main loop
    logic_fps = 30
    skip_ticks = 1000 / logic_fps # ticks between logic updates in milliseconds
    max_frameskip = 5 # minimum fps the game will run at before slowing down

    next_logic_tick = pygame.time.get_ticks()
    logical_loops = 0
    delta = 0.0 # used for interpolation when drawing

    while not game_over:

        logical_loops = 0
        while (pygame.time.get_ticks() > next_logic_tick and
                logical_loops < max_frameskip):
            
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

            # coconut creation
            if random.random() < lvl.blk_freq:
                speed = random.uniform(lvl.min_vel, lvl.max_vel)
                c = (Coconut(coconut_surf, [random.randint(lvl.left, lvl.right),
                    lvl.top], DIR_DOWN, speed, speed, lvl.bottom,
                    timeout=DEFAULT_TIMEOUT, expr=randexpr()))
                coconuts.add(c)
            # banana creation
            if random.random() < lvl.blk_freq:
                speed = random.uniform(lvl.min_vel, lvl.max_vel)
                b = (Banana(banana_surf, [random.randint(lvl.left, lvl.right),
                    lvl.top], DIR_DOWN, speed, speed, lvl.bottom,
                    timeout=DEFAULT_TIMEOUT))
                bananas.add(b)

            # update game state
            if lvl.blk_freq < lvl.blk_freq_max:
                lvl.blk_freq += lvl.blk_freq_inc

            # update sprites
            coconuts.update()
            bananas.update()

            # collision detection
            coconuts_collide_list = pygame.sprite.spritecollide(avatar,
                    coconuts, False)
            for c in coconuts_collide_list:
                if c.actionable(avatar):
                    print("Hit Coconut w/ expression: " + str(c.expr))
                    expr += c.expr
                    try:
                        print(str(expr) + " = " + str(expr.eval()))
                    except: pass
                    if avatar.lives > 0:
                        avatar.lives -= 1
                    else:
                        # go to game over screen and quit
                        bg_music.fadeout(3000)
                        full_screen_image(backdrops_folder + "game_over.png")
                        game_over = True
                    c.collided = True   # each coconut can only collide once
            bananas_collide_list = pygame.sprite.spritecollide(avatar,
                    bananas, False)
            for b in bananas_collide_list:
                if b.actionable(avatar):
                    b.collided = True   # each banana can only collide once
                    b.kill()
                    avatar.points += 1  # avatar gains 1 point for banana

            next_logic_tick += skip_ticks
            logical_loops += 1

        ############
        # DRAWING  #
        ############

        clk.tick()
        fps = clk.get_fps()

        delta = ((1.0 * pygame.time.get_ticks() + skip_ticks - next_logic_tick)
                 / skip_ticks)
        
        # draw sprites w/ delta movement

        screen.blit(lvl.bg_image, lvl.bg_rect)
        
        for c in coconuts:
            screen.blit(c.image, c.get_delta(delta))

        for b in bananas:
            screen.blit(b.image, b.get_delta(delta))

        screen.blit(avatar.image, avatar.get_delta(delta))
        blit_lives_icon(screen, avatar.lives)

        # draw text
        screen.blit(default_font.render(lvl.name, 1, COLOR_BLACK),
                level_display_pos)
        screen.blit(default_font.render('FPS: %.1f' % fps, 1, COLOR_BLACK),
                                        fps_display_pos)
        #screen.blit(default_font.render('Lives: %d' % avatar.lives, 1,
        #                               COLOR_BLACK), lives_display_pos)
        screen.blit(default_font.render('Points: %d' % avatar.points, 1,
                                        COLOR_BLACK), points_display_pos)
        # draw debug text
        screen.blit(default_font.render('blk_freq: %f' % lvl.blk_freq, 1,
                                        COLOR_BLACK), (20, 80))
        
        pygame.display.flip()
        
def randexpr():
    operators = ["+", "-"]
    operator_freq = .4

    a = 1
    b = 10

    if random.random() < operator_freq:
        return Expression([operators[random.randint(0, len(operators)-1)]])

    return Expression([random.randint(a, b)])

def blit_lives_icon(screen, lives):
    heart_file = icons_folder + 'heart.png'
    heart_surf = pygame.image.load(heart_file).convert_alpha()
    heart_rect = heart_surf.get_rect()
    heart_rect.topleft = (20, 20)
    x = 20
    y = 20
    for i in range(lives):
        if i > 14:
            break
        screen.blit(heart_surf, heart_rect)
        heart_rect.move_ip(32+8, 0)


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

