import pygame

class Game:
    """Keeps track of game state."""
    def __init__(self, lives = 0, points = 0):
        self.lives = 0
        self.points = 0

class Level:
    """Defines level settings such as difficulty."""
    
    def __init__(self, lvl_name = "Level X", bg_file="landscape.bmp",
                 time_limit = 120, max_blocks = -1,
                 min_vel = 2, max_vel = 10,
                 left = 0, top = 0, right = 640, bottom = 480,
                 items_dropped = [True, False]):
        
        self.lvl_name = lvl_name
        
        # level size
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        
        # build background image and rect
        self.bg_file = bg_file
        self.bg_image = pygame.image.load("resources/" + bg_file).convert()
        self.bg_rect = self.bg_image.get_rect()
        
        self.time_limit = time_limit    # seconds; -1 = infinity
        self.max_blocks = max_blocks    # -1 = infinity
        self.min_vel = min_vel          # velocity blocks fall
        self.max_vel = max_vel
        
        # items possibly dropped
        # [coconuts, bananas, ...]
        self.items_dropped = items_dropped


