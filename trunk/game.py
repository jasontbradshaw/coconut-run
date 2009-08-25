import pygame
import re

class Level:
    """Defines level settings such as difficulty."""
     
    def __init__(self, name = "Default", bg_file="landscape.bmp", time_limit =
            120, blk_freq_min = .015, blk_freq_max = 0.05, blk_freq_inc =
            0.00001, min_vel = 2, max_vel = 10, left = 0, top = 0, right = 800,
            bottom = 600, items_dropped = [True, False]):
        
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

        self.blk_freq = blk_freq_min
        self.blk_freq_inc = blk_freq_inc
        self.blk_freq_max = blk_freq_max
        
        # items possibly dropped
        # [coconuts, bananas, ...]
        self.items_dropped = items_dropped
    
    @staticmethod
    def load(file):
        """
        Returns a dict containing key/value pairs extracted from
        file, a text file with the following format:
            
            # a comment must begin with a hash at the
            # beginning of a line
            key:value
            key:value
            ...
        """

        # regex for extracting comments
        comment_re = re.compile('^#')

        with open(file, "r") as f:
            configs = dict()    # key/value storage
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    # skip blank lines
                    continue
                if comment_re.search(line) is not None:
                    # skip commented line
                    continue
                keyval = line.split(":")
                print keyval
                if len(keyval) == 2:
                    configs[keyval[0]] = keyval[1]
            return configs
                
class StateMachine(list):
    """
    Describes a set of states that one can traverse through.
    """
    def __init__(self, states, start=0):
        self.states = states
        self.start = start
        self.curr = start

    def add(self, state):
        self.states.append(state)

    def remove(self, state):
        # WARNING: untested funct
        if type(state) == int:
            # an int, remove that index
            del self.states[state]
        else:
            self.states.remove(state)

    def current(self, number=False):
        if number:
            return self.curr
        return self.states[self.curr]

    def change(self, s):
        """
        Changes the state to s.
        Returns True if state was changed, False if given illegal state
        """
        if type(s) == int:
            if s >= 0 and s < len(self):
                self.curr = s
                return True
        else:
            try:
                self.curr = self.states.index(s)
                return True
            except:
                pass
        return False

    def next(self):
        """
        Moves to the next state. Loops back around if at end of states list."""
        self.curr += 1
        if self.curr >= len(self):
            self.curr = 0
        return self.curr

    def reset(self):
        self.curr = self.start
    
    def __len__(self):
        return len(self.states)
