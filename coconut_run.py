import sys
import pygame
import pygame.gfxdraw
import random
import math
import copy
import os.path

from sprites import Droppable, Avatar, Coconut, Banana
from game import Level, StateMachine
from libcocorun import Expr, Op
import libcocorun

pygame.init()

# constants
DIR_RIGHT = 0
DIR_DOWN = 90
DIR_LEFT = 180
DIR_UP = 270

DEFAULT_TIMEOUT = 3000

resource_folder = 'resources'
audio_folder = os.path.join(resource_folder, 'audio')
graphics_folder = os.path.join(resource_folder, 'graphics')
avatar_folder = os.path.join(graphics_folder, 'avatar')
backdrops_folder = os.path.join(graphics_folder, 'backdrops')
droppable_folder = os.path.join(graphics_folder, 'droppable')
icons_folder = os.path.join(graphics_folder, 'icons')
items_folder = os.path.join(graphics_folder, 'items')
fonts_folder = os.path.join(resource_folder, 'fonts')
oprnd_folder = os.path.join(graphics_folder, 'op', 'numbers')
optr_folder = os.path.join(graphics_folder, 'op', 'operators')

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = pygame.Color(0x00, 0xaa, 0xcc, 128)
COLOR_RED = pygame.Color(0xff, 0x00, 0x00, 128)
COLOR_GREEN = pygame.Color(0x00, 0xff, 0x00, 128)

# GUI window
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
#screen = pygame.display.set_mode(size,
#        pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)


# text
default_font = pygame.font.Font(os.path.join(fonts_folder, "anmari.ttf"), 26)
large_font = pygame.font.Font(os.path.join(fonts_folder, "anmari.ttf"), 60)
expr_font = pygame.font.Font(os.path.join(fonts_folder,
    "Justus-Roman.ttf"), 26)

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p.x), int(-p.y+600)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    DEBUG_PLAY = False
    for a in argv:
        if a == "d" or a == "debug":
            DEBUG_PLAY = True
            print "DEBUG_PLAY set."

    # resources
    coconut_file = os.path.join(icons_folder, 'coconut_highres.png')
    banana_file = os.path.join(icons_folder, 'banana_highres.png')

    # clock, for fps info and timing
    clk = pygame.time.Clock()

    # keyboard delay before key repeats
    pygame.key.set_repeat(10, 0)

    # level
    lvl = Level(name="Level 1",
            bg_file=os.path.join(backdrops_folder, "landscape.png"),
            time_limit=20,
            blk_freq_min=0.0,
            blk_freq_max=0.05,
            blk_freq_inc=0.0001,
            min_vel=4, max_vel=7,
            left=0, top=0, right=width, bottom=height-100)
    expr = Expr()
    time_limit = lvl.time_limit

    #initialize mixer/music/sounds
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    bg_music = pygame.mixer.Sound(os.path.join(audio_folder,
        'sample_music.ogg'))
    hit_sound = pygame.mixer.Sound(os.path.join(audio_folder, 'pop2.wav'))
    
    channel = bg_music.play()
    
    
    # load surfaces
    coconut_surf = pygame.image.load(coconut_file).convert_alpha()
    banana_surf = pygame.image.load(banana_file).convert_alpha() 

    # set up avatar
    avatar_file = os.path.join(avatar_folder, 'still1.png')

    avatar_surf = pygame.image.load(avatar_file).convert_alpha()
    coco_still = StateMachine([avatar_surf])

    avatar_sm = StateMachine(["still", "right", "left", "catch", "throw"],
            start=0)
    avatar_speed = 10
    avatar_lives = 5
    avatar_collision_rect = avatar_surf.get_rect()
    avatar_collision_rect.width = 20
    avatar_collision_rect.height = 10
    avatar_collision_bottomleft = (32+5, lvl.bottom-60)
    avatar = Avatar(avatar_surf, image_bottomleft=(0, lvl.bottom),
            collision_rect=avatar_collision_rect,
            collision_bottomleft=avatar_collision_bottomleft,
            dir=0, vel=0, speed=avatar_speed,
            lives=avatar_lives, points=0, states=avatar_sm)
    avatar.set_frames(0, build_sm("still", 1, avatar_folder), mspf=300)
    avatar.set_frames(1, build_sm("right", 6, avatar_folder), mspf=80)
    avatar.set_frames(2, build_sm("left", 6, avatar_folder), mspf=80)
    avatar.set_frames(3, coco_still)
    avatar.set_frames(4, build_sm("scratch", 2, avatar_folder), mspf=200)

    # make groups
    coconuts = pygame.sprite.Group()
    bananas = pygame.sprite.Group()
    
    fps_display_pos = (lvl.right - 140, 20)
    level_display_pos = (lvl.right / 2 - 50, 20)
    bananas_display_pos = (20, 50)
    # points_display_pos = (20, 50)
    time_display_pos = (width/2 - 50, 20)

    # menus
    full_screen_image(os.path.join(backdrops_folder, "main_menu.png"))
    game_over = False
    
    # Current Game State
    already_pop = False  # Boolean to make sure d press only deletes 1 Op
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
            
            # Coco can't walk off screen
            if (avatar.left_pos() <= lvl.left or
                    avatar.right_pos() >= lvl.right):
                avatar.change("still")

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
                            avatar.change("left")
                            #avatar.move(DIR_LEFT, avatar.speed)
                    elif event.key == pygame.K_RIGHT:
                        if avatar.right_pos() < lvl.right:
                            avatar.change("right")
                            #avatar.move(DIR_RIGHT, avatar.speed)
                    elif event.key == pygame.K_d:
                        # remove last caught coconut
                        if (not already_pop and (banana_points >= 1 or
                            DEBUG_PLAY)):
                            if len(expr) > 0:
                                expr.pop()
                                already_pop = True
                                banana_points = banana_points - 1
                    elif event.key == pygame.K_b:
                        DEBUG_PLAY = not DEBUG_PLAY
                # Key Up
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        avatar.change("still")
                        avatar.vel = 0.0
                    if event.key == pygame.K_d:
                        already_pop = False

            # create coconut
            if random.random() < lvl.blk_freq:
                speed = random.uniform(lvl.min_vel, lvl.max_vel)
                c = (Coconut(coconut_surf, (random.randint(lvl.left,
                    lvl.right), lvl.top), DIR_DOWN, speed, speed,
                    lvl.bottom, timeout=DEFAULT_TIMEOUT, expr=randexpr()))
                coconuts.add(c)
            # create banana
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
                    c.kill()
                    Channel = hit_sound.play()
                    print("Hit Coconut w/ expression: " + str(c.expr))
                    expr.append(c.expr)
                    print(str(expr))
                    try:
                        print(str(expr) + " = " + str(expr.eval()))
                    except: pass
                    if False:
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

        time_limit = time_limit - ( clk.tick(60) * .001 )
        fps = clk.get_fps()

        delta = ((1.0 * pygame.time.get_ticks() + skip_ticks - next_logic_tick)
                 / skip_ticks)
        
        # draw sprites w/ delta movement

        screen.blit(lvl.bg_image, lvl.bg_rect)
        
        for c in coconuts:
            screen.blit(c.image, c.get_delta(delta))
            if DEBUG_PLAY:
                debug_draw_rect(screen, c.rect, COLOR_RED)
            op_surf = pygame.image.load(op_file(c.expr)).convert_alpha()
            screen.blit(op_surf, c.get_delta(delta))
        for b in bananas:
            screen.blit(b.image, b.get_delta(delta))
            if DEBUG_PLAY:
                debug_draw_rect(screen, b.rect, COLOR_GREEN)

        # draw avatar
        avatar_rect = avatar.get_delta(delta)
        screen.blit(avatar.image, avatar_rect)
        blit_bananas_icon(screen, 1)

        if DEBUG_PLAY:
            debug_draw_rect(screen, avatar.rect, COLOR_BLUE)

        # draw expression
        expr_txt = ""
        if expr.valid():
          expr_txt += str(expr.eval()) + " = "
        expr_txt += str(expr)
        screen.blit(expr_font.render(expr_txt, True, COLOR_BLACK), (40, 450))
        draw_expr(screen, expr)

        # draw Level Name
        #screen.blit(default_font.render(lvl.name, True, COLOR_BLACK),
        #    level_display_pos)
        # draw Bananas
        screen.blit(default_font.render('     x %d' % banana_points,
            True, COLOR_BLACK), bananas_display_pos)       
        # draw Time
        screen.blit(large_font.render('% 3d' % time_limit,
            True, COLOR_BLACK), time_display_pos)
        # draw debug text
        if DEBUG_PLAY:
            screen.blit(default_font.render('FPS: %.1f' % fps, True,
                COLOR_BLACK), fps_display_pos)
            screen.blit(default_font.render('blk_freq: %f' % lvl.blk_freq,
                True, COLOR_BLACK), (20, 80))

        pygame.display.flip()

def draw_expr(screen, expr, rect=None):
    if rect is None:
        rect = pygame.Rect(40, 600-60, 32, 32)
    for e in expr:
        if e.oprnd() or e.optr():
            pygame.gfxdraw.box(screen, rect, COLOR_BLUE)
            op_surf = pygame.image.load(op_file(e)).convert_alpha()
            screen.blit(op_surf, rect)
            s = e
            if e == '*':
                s = 'x'
            screen.blit(large_font.render(s, True, COLOR_BLACK),
                    (rect.x, rect.y))
            rect.left += 40
        else:
            draw_expr(screen, e, rect)

def op_file(op):
    if op.oprnd():
        return os.path.join(oprnd_folder, op+'.png')
    elif op.optr():
        if op == '+':
            return os.path.join(optr_folder, 'addition.png')
        elif op == '-':
            return os.path.join(optr_folder, 'subtraction.png')
        elif op == '*':
            return os.path.join(optr_folder, 'multiply.png')
        elif op == '/':
            return os.path.join(optr_folder, 'divide.png')
    return os.path.join(optr_folder, 'multiplication.png')

def blit_bananas_icon(screen, num):
    banana_file = os.path.join(icons_folder, 'banana_highres.png')
    banana_surf = pygame.image.load(banana_file).convert_alpha()
    banana_rect = banana_surf.get_rect()
    banana_rect.topleft = (20, 50)
    for i in range(num):
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

def randexpr(min=0, max=9, operator_freq=0.25, unary=False):
    ops = libcocorun.binary_optrs
    if unary:
        ops = libcocorun.operators

    if random.random() < operator_freq:
        # make operator
        return Op(ops[random.randint(0, len(ops)-1)])
    # return operand
    return Op(str(random.randint(min, max)))

def build_sm(statename, num_frames=1, folder=""):
    # builds a StateMachine animation for a given statename.
    # This function breaks quite easily, so be careful!
    # How to use:
    #  if statename="dance" and num_frames=4, then we build a list
    #  using files dance1.png, dance2.png, ...
    anim_list = []
    for i in range(1,num_frames+1):
        file = os.path.join(folder, statename+str(i)+'.png')
        surf = pygame.image.load(file).convert_alpha()
        anim_list.append(surf)
    return StateMachine(anim_list)

def debug_draw_rect(screen, rect, color):
    points = [rect.topleft, rect.topright,
            rect.bottomright, rect.bottomleft]
    pygame.gfxdraw.filled_polygon(screen, points, color)


if __name__ == "__main__":
    sys.exit(main())
