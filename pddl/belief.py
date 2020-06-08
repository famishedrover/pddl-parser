"""
Classes related to initial belief model.
"""

from typing import Union, List
from .formula import AtomicFormula, NotFormula
Literal = Union[AtomicFormula,NotFormula]

class UnknownLiteral(object):
    """ Unknown literal

    :param formula: the unknown literal
    """
    def __init__(self, formula: AtomicFormula):
        self.__formula = formula

    @property
    def formula(self) -> AtomicFormula:
        return self.__formula

    def __str__(self):
        return '(unknown ' + str(self.formula) + ')'

class OrBelief(object):
    """ Choice belief

    :param literals: possible initial believes
    """
    def __init__(self, literals: List[Literal]):
        self.__literals = literals

    @property
    def literals(self) -> List[Literal]:
        return self.__literals

    def __str__(self):
        pddl = '(or'
        for a in self.literals:
            pddl += ' ' + str(a)
        pddl += ')'
        return pddl

class OneOfBelief(object):
    """ Exclusive choice belief

    :param literals: possible exclusive initial believes
    """
    def __init__(self, literals: List[Literal]):
        self.__literals = literals

    @property
    def literals(self) -> List[Literal]:
        return self.__literals

    def __str__(self):
        pddl = '(oneof'
        for a in self.literals:
            pddl += ' ' + str(a)
        pddl += ')'
        return pddl
