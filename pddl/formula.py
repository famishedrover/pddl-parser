"""
PDDL basic classes representing literals, terms, goals, ...
"""

from typing import List, Union
Goal = Union['AtomicFormula', 'NotFormula', 'AndFormula']

class AtomicFormula(object):
    """ (predicate <argument>*)

    :param predicate: predicate name
    :param arguments: formula arguments
    """
    def __init__(self, predicate: str, arguments: List[str] = []):
        self.__predicate = predicate
        self.__arguments = arguments

    @property
    def name(self) -> str:
        return self.__predicate

    @property
    def arguments(self) -> List[str]:
        return self.__arguments

    def __str__(self):
        pddl = '(' + self.name
        for a in self.arguments:
            pddl += ' ' + str(a)
        pddl += ')'
        return pddl

class NotFormula(object):
    """ (not <formula>)

    :param formula: negated formula
    """
    def __init__(self, formula: AtomicFormula):
        self.__formula = formula

    @property
    def formula(self) -> AtomicFormula:
        return self.__formula

    def __str__(self):
        return  '(not ' + str(self.formula) + ')'

class AndFormula(object):
    """ (and <formula>*)

    :param formulas: list of formulas in conjunction
    """
    def __init__(self, formulas: List[Goal]):
        self.__formulas = formulas

    @property
    def formulas(self) -> List[Goal]:
        return self.__formulas

    def __str__(self):
        pddl = '(and'
        for a in self.formulas:
            pddl += ' ' + str(a)
        pddl += ')'
        return pddl

class WhenEffect(object):
    """ Conditional effect

    :param condition: condition
    :param effect: effect
    """
    def __init__(self,
                 condition: Goal,
                 effect: Union[AtomicFormula,AndFormula]
                 ):
        self.__condition = condition
        self.__effect = effect

    @property
    def condition(self) -> Goal:
        return self.__condition

    @property
    def effect(self) -> Union[AtomicFormula,AndFormula]:
        return self.__effect

    def __str__(self):
        return '(when ' + str(self.condition) + ' ' + str(self.effect) + ')'
