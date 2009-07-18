import sys
import os
sys.path.append( os.path.join( os.getcwd(), '..' ) )
from libcocorun import Expr
from libcocorun import Op

plus = Op("+")
minus = Op("-")
divide = Op("/")
times = Op("*")
power = Op("**")
mod = Op("%")
sin = Op("math.sin")
exp = Op("math.exp")
log = Op("math.log")

one = Op("1")
two = Op("2")
three = Op("3")
four = Op("4")
ten = Op("10")
nan = Op("a")
nan2 = Op("bb")

e1 = Expr([one, plus, two])
e2 = Expr([two, times, three, plus, one])
e3 = Expr([two, power, four, four])
e4 = Expr([two, times])

valid = []
valid.append(Expr([one]))
valid.append(Expr([ten]))
valid.append(Expr([one, plus, two]))
valid.append(Expr([one, plus, two, times, three]))
valid.append(Expr([e1, times, e1]))
valid.append(Expr([e2, times, two]))
valid.append(Expr([e2, plus, e2, times, e1, times, two, power, three, minus,
    four, plus, two, times, e1]))
valid.append(Expr([log, two]))

invalid = []
invalid.append(Expr([one, two]))
invalid.append(Expr([e4, times, e3]))
invalid.append(Expr([times]))
invalid.append(Expr([times, one]))
invalid.append(Expr([one, times]))
invalid.append(Expr([log, exp, two])) # should be [log, [exp, two]]

print "=== Valid: ==="
for e in valid:
    print str(e),
    if e.valid():
        print "=", str(e.eval())
    else:
        print "is Invalid."

print "=== Invalid: ==="
for e in invalid:
    print str(e),
    if e.valid():
        print "=", str(e.eval())
    else:
        print "is Invalid."
