class Primitive:
    def __init__(self, sym="", desc=""):
        self.sym = sym
        self.desc = desc

class Expression:
    def __init__(self):
        self.expr = []
    
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

