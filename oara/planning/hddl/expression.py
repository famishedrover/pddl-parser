from typing import List, Union
from abc import ABC

from .formula import AtomicFormula


class FluentExpression(ABC):
    """ A Fluent expression."""
    pass


class Number(FluentExpression):
    """ Number.

    :param value: value
    """
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return self.__value


class FunctionExp(FluentExpression, AtomicFormula):
    """ Fluent predicate call.

    f_head : func_symbol | '(' func_symbol term* ')';
    """
    pass


class EqualityExp(FluentExpression, AtomicFormula):
    """ Equality.

    num_init : equallity f_head NUMBER ')';

    """
    def __init__(self, f_head: FluentExpression, number: Number):
        self.__f = f_head
        self.__number = number

    def __str__(self) -> str:
        return f"(= {self.__f} {self.__number})"


class OppositeExp(FluentExpression):
    """ Oppositve expression.

    '(' '-' f_exp ')'

    :param expression: base expression
    """
    def __init__(self, expression: FluentExpression):
        self.__expression = expression

    def __str__(self):
        return f"( - {self.__expression} )"


class AdditionExp(FluentExpression):
    """ Addition.

    :param expressions: expressions to add.
    """
    def __init__(self, expressions: List[FluentExpression]):
        self.__expressions = expressions

    def __str__(self):
        return f"( + {' '.join(self.__expressions)})"


class MultiplicationExp(FluentExpression):
    """ Multiplication.

    :param expressions: expressions to multiply.
    """
    def __init__(self, expressions: List[FluentExpression]):
        self.__expressions = expressions

    def __str__(self):
        return f"( * {' '.join(self.__expressions)})"


class SubstractionExp(FluentExpression):
    """ Substraction.

    :param expressions: expressions to substract.
    """
    def __init__(self, expressions: List[FluentExpression]):
        self.__expressions = expressions

    def __str__(self):
        return f"( - {' '.join(self.__expressions)})"


class DivisionExp(FluentExpression):
    """ Division.

    :param expressions: expressions to divide.
    """
    def __init__(self, expressions: List[FluentExpression]):
        self.__expressions = expressions

    def __str__(self):
        return f"( / {' '.join(self.__expressions)})"
