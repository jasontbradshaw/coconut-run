class Symbol:
    def __init__(self, sym=""):
        self.sym = sym

class Expression:
    def __init__(self, expr = [], goal = 0):
        self.expr = expr
        self.goal = goal
    
    def insert(self, i, p):
        self.expr.insert(i, p)

    def append(self, p):
        self.expr.append(p)

    def remove(self):
        return self.expr.pop();

    def eval(self):
        return eval(self.__str__())

    def __str__(self):
        str = ""
        for e in self.expr:
            str = str + e.sym
        return str

    def valid(self):
        if self.eval() == valid:
            print "VALID!"
            return True
        return False
