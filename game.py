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

class Music:
    """A silly wrapper around pygame.mixer.music."""

    def __init__(self, filename=""):
        self.filename = filename
        pygame.mixer.music.load(filename)

    def play(self, loops=-1, start=0):
        pygame.mixer.music.play(loops, start)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()
    
    def fadeout(self, time):
        pygame.mixer.music.fadeout(time)
