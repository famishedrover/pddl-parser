"""PDDL basic classes representing literals, terms, goals, ..."""

from typing import List, Union
from .variable import Variable


class Number:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Function:
    def __init__(self, func_symbol, parameters: List = []):
        self.function = func_symbol
        self.parameters = parameters

    def __str__(self):
        return f'( {self.function} {" ".join(self.parameters)} )'


class UnaryOp:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"( {self.op} {self.expr} )"


class MultiOp:
    def __init__(self, op, expressions: List):
        self.op = op
        self.exprs = expressions

    def __str__(self):
        return f"( {self.op} {' '.join(self.exprs)} )"

