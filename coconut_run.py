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
from game import StateMachine
from libcocorun import Expr
from libcocorun import Op
import libcocorun

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

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# GUI window
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    # resources
    #coconut_file = droppable_folder + 'coconut.png'
    coconut_file = icons_folder + 'coconut_highres.png'
    #banana_file = droppable_folder + 'banana.png'
    banana_file = icons_folder + 'banana_highres.png'

    # clock, for fps info and timing
    clk = pygame.time.Clock()

    # keyboard delay before key repeats
    pygame.key.set_repeat(10, 0)

    # level
    lvl = Level(name = "Level 1",
            bg_file = backdrops_folder + "landscape.png",
            time_limit = 120,
            blk_freq_min = 0.015,
            blk_freq_max = 0.10,
            blk_freq_inc = 0.0001,
            min_vel = 5, max_vel = 10,
            left = 0, top = 0, right = width, bottom = height - 40)
    expr = Expr()
    time_limit = lvl.time_limit

    #initialize mixer/music/sounds
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    bg_music = pygame.mixer.Sound(audio_folder + 'sample_music.ogg')
    hit_sound = pygame.mixer.Sound(audio_folder + 'pop2.wav')
    
    channel = bg_music.play()
    
    
    # load surfaces
    coconut_surf = pygame.image.load(coconut_file).convert_alpha()
    banana_surf = pygame.image.load(banana_file).convert_alpha() 

    # set up avatar
    avatar_file = avatar_folder + 'avatar.png'
    coco1 = avatar_folder + 'pain1.png'
    coco2 = avatar_folder + 'pain2.png'

    avatar_surf = pygame.image.load(avatar_file).convert_alpha()
    coco_surf1 = pygame.image.load(coco1).convert_alpha()
    coco_surf2 = pygame.image.load(coco2).convert_alpha()
    coco_still = StateMachine([avatar_surf])
    coco_pain = StateMachine([coco_surf1, coco_surf2])

    avatar_sm = StateMachine(["still", "bored"], start=0)
    avatar_rect = avatar_surf.get_rect()
    avatar_speed = 15
    avatar_lives = 5
    avatar = Avatar(avatar_surf, (0, lvl.bottom),
                    0, 0, avatar_speed, avatar_lives, 0, avatar_sm)
    avatar.set_frames(0, coco_still)
    avatar.set_frames(1, coco_pain)

    # make groups
    coconuts = pygame.sprite.Group()
    bananas = pygame.sprite.Group()

    # text
    default_font = pygame.font.Font(fonts_folder + "anmari.ttf", 26)
    expr_font = pygame.font.Font(fonts_folder + "Justus-Roman.ttf", 26)
    
    fps_display_pos = (lvl.right - 140, 20)
    level_display_pos = (lvl.right / 2 - 50, 20)
    bananas_display_pos = (20, 50)
    # points_display_pos = (20, 50)
    time_display_pos = (20, 20)

    # menus
    full_screen_image(backdrops_folder + "main_menu.png")
    game_over = False
    
    # Current Game State
    already_pop = True  # Boolean to make sure d press only deletes 1 Op
    banana_points = 0

    # main loop
    logic_fps = 30
    skip_ticks = 1000 / logic_fps # ticks between logic updates in milliseconds
    max_frameskip = 5 # minimum fps the game will run at before slowing down

    next_logic_tick = pygame.time.get_ticks()
    logical_loops = 0
    delta = 0.0 # used for interpolation when drawing

    clk.tick() # Allows the seconds passed to be calculated

    while not game_over:

        logical_loops = 0
        while (pygame.time.get_ticks() > next_logic_tick and
                logical_loops < max_frameskip):
            
            ############
            #  LOGIC   #
            ############

            avatar.update()
            avatar.update_image()
            
            # input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # Key Down
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_LEFT: # do these last!
                        if avatar.left_pos() > lvl.left:
                            avatar.move(180, avatar.speed)
                    elif event.key == pygame.K_RIGHT:
                        if avatar.right_pos() < lvl.right:
                            avatar.move(0, avatar.speed)
                    if (event.key == pygame.K_d and already_pop
                            and banana_points >= 1):
                        avatar.change("bored")
                        if len(expr) > 0:
                            expr.pop()
                            already_pop = False
                            banana_points = banana_points - 1
                # Key 
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        avatar.vel = 0.0
                    if event.key == pygame.K_d:
                        avatar.change("still")
                        already_pop = True
                        

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
                    Channel = hit_sound.play()
                    print("Hit Coconut w/ expression: " + str(c.expr))
                    expr.append(c.expr)
                    print(str(expr))
                    try:
                        print(str(expr) + " = " + str(expr.eval()))
                    except: pass
                    if avatar.lives > 0:
                        pass # don't lose lives
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
                    banana_points += 1  # gains 1 banana point

            next_logic_tick += skip_ticks
            logical_loops += 1

        ############
        # DRAWING  #
        ############

        time_limit = time_limit - ( clk.tick() * .001 )
        fps = clk.get_fps()

        delta = ((1.0 * pygame.time.get_ticks() + skip_ticks - next_logic_tick)
                 / skip_ticks)
        
        # draw sprites w/ delta movement

        screen.blit(lvl.bg_image, lvl.bg_rect)
        
        for c in coconuts:
            screen.blit(c.image, c.get_delta(delta))
            screen.blit(expr_font.render(str(c.expr), True, COLOR_WHITE,
              COLOR_BLACK), c.get_delta(delta))

        for b in bananas:
            screen.blit(b.image, b.get_delta(delta))

        screen.blit(avatar.image, avatar.get_delta(delta))
        blit_bananas_icon(screen, 1)

        # draw expression
        expr_txt = ""
        if expr.valid():
          expr_txt += str(expr.eval()) + " = "
        expr_txt += str(expr)
        screen.blit(expr_font.render(expr_txt, True, COLOR_BLACK), (40, 450))

        # draw Level Name
        screen.blit(default_font.render(lvl.name, True, COLOR_BLACK),
            level_display_pos)
        # draw FPS
        screen.blit(default_font.render('FPS: %.1f' % fps, True,
            COLOR_BLACK), fps_display_pos)
        # draw Bananas
        screen.blit(default_font.render('     x %d' % banana_points,
            True, COLOR_BLACK), bananas_display_pos)       
        # draw Time
        screen.blit(default_font.render('Time: %d sec' % time_limit,
            True, COLOR_BLACK), time_display_pos)
        # draw debug text
        screen.blit(default_font.render('blk_freq: %f' % lvl.blk_freq,
            True, COLOR_BLACK), (20, 80))

        pygame.display.flip()
        

def blit_bananas_icon(screen, lives):
    banana_file = icons_folder + 'banana_highres.png'
    banana_surf = pygame.image.load(banana_file).convert_alpha()
    banana_rect = banana_surf.get_rect()
    banana_rect.topleft = (20, 50)
    for i in range(lives):
        if i > 14:
            break
        screen.blit(banana_surf, banana_rect)
        banana_rect.move_ip(32+8, 0)


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


def randexpr(min=0, max=10, operator_freq=0.25):
    if random.random() < operator_freq:
        # make operator
        return Op(libcocorun.operators[random.randint(0,
          len(libcocorun.operators)-1)])
    # return operand
    return Op(str(random.randint(min, max)))

if __name__ == "__main__":
    pygame.init()
    sys.exit(main())
event.key == pygame.K_d
