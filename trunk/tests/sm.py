import sys
import os
sys.path.append( os.path.join( os.getcwd(), '..' ) )
from game import StateMachine

states = ["still", "move left", "move right", "dead", "bored"]
sm = StateMachine(states)

print "1:", (len(sm) == 5)
print "2:", (sm.current() == "still")
sm.change(4)
print "3:", (sm.current() == "bored")
sm.change(2)
print "4:", (sm.current() == "move right")
print "5:", (sm.current(True) == 2)
sm.change(1)
print "6:", (sm.current() == "move left")
sm.reset()
print "7:", (sm.current() == "still")
sm.change(-1)
print "8:", (sm.current() == "still")
sm.next()
sm.next()
print "9:", (sm.current() == "move right")
sm.reset()
print "10:", (sm.current(True) == 0)
sm.change("dead")
print "11:", (sm.current() == "dead")
