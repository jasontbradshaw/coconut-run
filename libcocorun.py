import random
import math

binary_optrs = ['+', '-', '*', '/', '**', '%']
unary_optrs = ['sin']
operators = binary_optrs #binary_optrs & unary_ops

class Op(str):
    """
    The Op class holds an operand or operator, depending on the content of the
    string.
    """

    def oprnd(self):
        return self not in operators
        # TODO: use regular expressions so we can take decimal numbers
        """for c in self:
            if c < '0' or c > '9':
                return False
        return True"""

    def optr(self):
        return self in operators

    def binary_optr(self):
        return self in binary_optrs
    
    def unary_optr(self):
        return self in unary_optrs

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

        self = [] is invalid
        
        for every e in self:
          e is expr ==>
            e is valid
            e first element ==> right(e) is binary optr
            e last element ==> left(e) is optr
            e not (first or last) element ==>
              left(e) is optr and right(e) is binary optr
          e is optr ==>
            e is binary optr ==>
              e not first or last
              left(e) and right(e) is oprnd or valid expr
            e is unary optr ==>
              e not first ==> left(e) is optr
              right(e) is oprnd or valid expr
          e is oprnd ==>
            e is first ==> right(e) is binary optr
            e is last ==> left(e) is optr
            e is not first or last ==> left(e) and right(e) is optr
        """

        if len(self) == 0:
            return False

        for i in range(len(self)):
            e = self[i]
            left = None
            right = None

            if i > 0:
                left = self[i-1]
            if i < len(self)-1:
                right = self[i+1]

            if type(e) == Expr:
                if not e.valid():
                    return False
                if i == 0 and not (type(right) == Op and right.binary_optr()):
                    return False
                if i == len(self)-1 and not (type(left) == Op and left.optr()):
                    return False
                if (i != 0 and i != len(self)-1 and not
                    (type(left) == Op and type(right) == Op and
                    left.optr() and right.binary_optr())):
                    return False
            elif type(e) == Op and e.optr():
                if e.binary_optr():
                    if i == 0 or i == len(self)-1:
                        return False
                    if (not (((type(right) == Op and right.oprnd()) or
                        (type(right) == Expr and right.valid())) and
                        ((type(left) == Op and left.oprnd()) or
                        (type(left) == Expr and left.valid())))):
                        return False
                elif e.unary_optr():
                    if i == len(self)-1:
                        return False
                    if i > 0 and not ((type) == Op and left.optr()):
                        return False
                else:
                    raise InvalidExpr("Expression Engine: operator not a\\
                            binary or unary operator!")
                    print "An operator not in binary and not in unary!"
            elif type(e) == Op and e.oprnd():
                if len(self) == 1:
                    return True
                if i == 0 and not (type(right) == Op and right.binary_optr()):
                    return False
                if i == len(self)-1 and not (type(left) == Op and left.optr()):
                    return False
                if (i != 0 and i != len(self)-1 and not (type(left) == Op and
                    left.optr() and type(right) == Op and right.optr())):
                    return False
            else:
                # screwed up!
                raise InvalidExpr("Expression Engine: not an operator, \\
                operand, or expression!")
        return True

    def __str__(self):
        # TODO: if unary operator, add ()'s around the next expression.
        out = ""
        for e in self:
            if type(e) == Expr:
                out += "(" + str(e) + ")"
            else:
                out += str(e)
        return out


class InvalidExpr(Exception):
    pass
