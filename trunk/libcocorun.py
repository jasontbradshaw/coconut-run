import random

binary_ops = ['+', '-', '*', '/', '**', '%']
unary_ops = ['++']
operators = binary_ops #binary_ops & unary_ops

class Expr(list):
    """
    An Expr is used to hold a mathematical (though it can be any valid
    Python) expression. An Expr holds a list of Expressions.

    It's a list with a couple of useful functions for evaluating a
    mathematical expression.
    """
        
    def eval(self):
        if len(self) == 0:
            return 0
        if self.valid():
            # calls the python eval()
            return eval(str(self))
        else:
            raise InvalidExpr
            
    def valid(self):
        """
        Returns True if self is valid.

        self = [] is valid
        self = [x] is valid iff x is valid
        
        for self = [x:xs]: for every e in self,
       
        e is a binary operator ==>
            (e is not first or last element) and (left(e) and right(e) are
            expressions)
        e is a unary operator ==>
            e is not last element and right(e) is an expression
        e is an expression ==>
            e is valid
            e is first element ==> right(e) is binary operator
            e is last element ==> left(e) is operator
            e is not(first or last) ==> right(e) and left(e) are operators
        
        """
        if len(self) == 0:
            return True
        if type(self) is str:
            # turtle all the way down to strings
            if self in operators:
                return False
            return True

        for i in range(len(self)):
            e = self[i]
            left = None
            right = None

            if i > 0:
              left = self[i-1]
            if i < len(self)-1:
              right = self[i+1]

            if str(e) in binary_ops:
                if (i == 0 or i == len(self)-1 or not left.valid() or not
                right.valid()):
                    # invalid binary operator
                    return False
            elif str(e) in unary_ops:
                if i == len(self)-1 or not right(e).valid():
                    # invalid unary operator
                    return False
            else: # an expression
                if len(e) == 1 and e not in operators:
                    # a number
                    continue
                if not e.valid():
                    return False
                elif i == 0 and str(right) not in binary_ops:
                    return False
                elif i == len(self)-1 and str(left) not in operators:
                    return False
                elif (i != 0 and i != len(self)-1 and (str(left) not in
                    operators or str(right) not in operators)):
                    return False
        return True

    def __str__(self):
        str = ""
        for e in self:
            str += e.__str__()
        return str


class InvalidExpr(Exception):
    pass
