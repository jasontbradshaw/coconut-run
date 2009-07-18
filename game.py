import pygame

class Level:
    """Defines level settings such as difficulty."""
    
    def __init__(self, name = "Default", bg_file="landscape.bmp",
                 time_limit = 120,
                 blk_freq = .015, blk_freq_inc = 0.00001, blk_freq_max = 0.05,
                 min_vel = 2, max_vel = 10,
                 left = 0, top = 0, right = 640, bottom = 480,
                 items_dropped = [True, False]):
        
        self.name = name
        
        # level size
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        
        # build background image and rect
        self.bg_file = bg_file
        self.bg_image = pygame.image.load(bg_file).convert()
        self.bg_rect = self.bg_image.get_rect()
        
        self.time_limit = time_limit    # seconds; -1 = infinity
        self.min_vel = min_vel          # velocity blocks fall
        self.max_vel = max_vel

        self.blk_freq = blk_freq
        self.blk_freq_inc = blk_freq_inc
        self.blk_freq_max = blk_freq_max
        
        # items possibly dropped
        # [coconuts, bananas, ...]
        self.items_dropped = items_dropped

class StateMachine:
    def __init__(self, states = [], start = 0):
        self.states = states
        self.start = start
        self.curr = start

    def num_states(self):
        return len(self.states)

    def current(self, number=False):
        if number:
            return self.curr
        return self.states[self.curr]

    def change(self, s):
        if type(s) == str:
            try:
                self.curr = self.states.index(s)
                return True
            except:
                return False
        elif type(s) == int:
            if s >= 0 and s < self.num_states():
                self.curr = s
                return True
            return False
        return False

    def reset(self):
        self.curr = self.start

