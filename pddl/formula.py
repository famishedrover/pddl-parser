"""PDDL basic classes representing literals, terms, goals, ..."""

from typing import List, Union
GOAL = Union['AtomicFormula', 'NotFormula', 'AndFormula']


class AtomicFormula:

    """(predicate <argument>*).

    :param predicate: predicate name
    :param arguments: formula arguments
    """

    def __init__(self, predicate: str, arguments: List[str] = ()):
        self.__predicate = predicate
        self.__arguments = arguments

    @property
    def name(self) -> str:
        """Get name."""
        return self.__predicate

    @property
    def arguments(self) -> List[str]:
        """Get arguments."""
        return self.__arguments

    def __str__(self):
        pddl = '(' + self.name
        for arg in self.arguments:
            pddl += ' ' + str(arg)
        pddl += ')'
        return pddl


class NotFormula:

    """(not <formula>).

    :param formula: negated formula
    """

    def __init__(self, formula: AtomicFormula):
        self.__formula = formula

    @property
    def formula(self) -> AtomicFormula:
        """Get negated formula."""
        return self.__formula

    def __str__(self):
        return '(not ' + str(self.formula) + ')'


class AndFormula:

    """(and <formula>*).

    :param formulas: list of formulas in conjunction
    """

    def __init__(self, formulas: List[GOAL]):
        self.__formulas = formulas

    @property
    def formulas(self) -> List[GOAL]:
        """Get formulas."""
        return self.__formulas

    def __str__(self):
        pddl = '(and'
        for formula in self.formulas:
            pddl += ' ' + str(formula)
        pddl += ')'
        return pddl


class WhenEffect:

    """Conditional effect.

    :param condition: condition
    :param effect: effect
    """

    def __init__(self,
                 condition: GOAL,
                 effect: Union[AtomicFormula, AndFormula]):
        self.__condition = condition
        self.__effect = effect

    @property
    def condition(self) -> GOAL:
        """Get condition."""
        return self.__condition

    @property
    def effect(self) -> Union[AtomicFormula, AndFormula]:
        """Get effect."""
        return self.__effect

    def __str__(self):
        return '(when ' + str(self.condition) + ' ' + str(self.effect) + ')'
