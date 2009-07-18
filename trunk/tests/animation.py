import sys
import os
sys.path.append( os.path.join( os.getcwd(), '..' ) )
from sprites import Animation

s = ["right foot", "left foot", "turn around", "sit down!"]
a = Animation(s1)
print (len(a) == 4)
print (a.current() == "right foot")
a.next()
print (a.current() == 1)

