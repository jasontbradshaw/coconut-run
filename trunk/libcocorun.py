class Symbol:
    def __init__(self, sym=""):
        self.sym = sym

class Expression(list):
    """
    An Expression is used to hold a mathematical (though it can be any valid
    Python) expression. An Expression holds a list of Expressions.

    It's a list with a couple of useful functions for evaluating a
    mathematical expression.
    """

    binary = frozenset(['+', '-'])
    unary = frozenset(['++'])
    operators = binary & unary

    def eval(self):
        try:
            return eval(str(self))
        except:
            raise InvalidExpression
            
    # WARNING: not tested!
    def valid(self):
        for i in range(len(self)):
            e = self[i]
            if str(e) in binary:
                if i == 0 or i == len(self)-1:
                    # binary ops can't be first or last element
                    return False
                elif not (self[i-1].valid() and self[i+1].valid()):
                    # left or right is not valid
                    return False
            elif str(e) in unary:
                pass
        return True

    def __str__(self):
        str = ""
        for e in self:
            str = str + e.__str__()
        return str

class InvalidExpression(Exception):
    pass
