import random
import math

binary_optrs = ['+', '-', '*', '/', '**', '%']
unary_optrs = ['math.sin', 'math.exp', 'math.log']
operators = binary_optrs + unary_optrs

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

    # self is not an Expr
    def expr(self):
        return False

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
              e not first ==> left(e) is binary optr
              right(e) is oprnd or valid expr
          e is oprnd ==>
            e is first ==> right(e) is binary optr
            e is last ==> left(e) is optr
            e is not first or last ==> left(e) and right(e) is optr

        Note: the unary operator is currently limited. A unary operator can
        only have a binary operator or nothing to its left. It can only have a
        valid expression or an operand to its right.

        This is a limitation of __str__() not being able to put closing
        parenthesis properly. We would need a stack to do this, but is this
        something we want?
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

            if e.expr():
                if not e.valid():
                    return False

                # e is a valid expression, so make sure that it is flanked by
                # correct type of operators:

                if i == 0 and not right.binary_optr():
                    return False
                if i == len(self)-1 and not left.optr():
                    return False
                if (i != 0 and i != len(self)-1 and not (left.optr() and
                    right.binary_optr())):
                    # not at either ends, but not surrounded by proper optrs
                    return False
            elif e.optr():
                # e is an operator (e.g. +, *, sin, etc)
                if e.binary_optr():
                    # examples: +, *, /
                    if i == 0 or i == len(self)-1:
                        # no operands to operator on
                        return False
                    if (not (((right.oprnd()) or right.valid()) and
                        left.oprnd() or left.valid())):
                        # binary operators not flanked by valid operands or
                        # expressions
                        return False
                elif e.unary_optr():
                    # examples: sin(), exp()
                    if i == len(self)-1:
                        # doesn't have anythign to operator on
                        return False
                    if i > 0 and not left.binary_optr():
                        return False
                    if not(right.oprnd() or right.expr()):
                        return False
                else:
                    s = "Expression Engine: operator not a binary or unary"
                    s += " operator!"
                    raise InvalidExpr(s)
            elif e.oprnd():
                # an operand (e.g. 3, 3.1415, -42)
                if len(self) == 1:
                    # expression with one element is valid if that element is
                    # an operand
                    return True
                if i == 0 and not right.binary_optr():
                    # first element, but right side is not a binary operator
                    return False
                if i == len(self)-1 and not left.optr():
                    # last element, but left side is not an operator
                    return False
                if (i != 0 and i != len(self)-1 and not (left.optr() and
                    right.binary_optr())):
                    # not flanked by proper operators
                    return False
            else:
                s = "Expression Engine: not an operator, operand, or expression!"
                raise InvalidExpr(s)
        return True
    
    def expr(self):
        # self is an Expr
        return True
    def oprnd(self):
        return False
    def binary_optr(self):
        return False
    def unary_optr(self):
        return False
    def optr(self):
        return False

    def __str__(self):
        # TODO: if unary operator, add ()'s around the next expression.
        add_right_paren = 0
        out = ""
        for e in self:
            if e.expr():
                out += "(" + str(e) + ")"
            elif e.unary_optr():
                out += str(e) + "("
                add_right_paren += 1
                continue
            else:
                out += str(e)
            if add_right_paren > 0:
                out += ")" * add_right_paren
                add_right_paren = 0
        return out

class InvalidExpr(Exception):
    pass
