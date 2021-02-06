from typing import List, Union
from abc import ABC

from .types import TypedVariable
from .formula import LITERAL, AtomicFormula
from .expression import FluentExpression
from .gd import GD


class AbstractEffect(ABC):
    """ Abstract Effect Formula. """
    pass


class EmptyEffect(AbstractEffect):
    """ Empty Effect. """
    def __str__(self):
        return '()'


class ConjunctionEffect(AbstractEffect):
    """ Conjunction effect.

    eff_conjunction : '(' 'and' effect+ ')';

    :param effects: list of formulas in conjunction
    """
    def __init__(self, effects: List['EFFECT']):
        self.__effects = effects

    @property
    def effects(self) -> List['EFFECT']:
        return self.__effects

    def __str__(self):
        nltab = '\n\t\t'
        return f"""(and
            {nltab.join(map(str, self.__effects))}
        )"""


class UniversalEffect(AbstractEffect):
    """ Universal effect.

    eff_universal : '(' 'forall' '(' typed_var_list ')' effect ')';

    :param variables: list of variables in universal
    :param effect: effect
    """
    def __init__(self, variables: List[TypedVariable], effect: 'LITERAL'):
        self.__variables = variables
        self.__effect = effect

    @property
    def variables(self) -> List[TypedVariable]:
        return self.__variables

    @property
    def effect(self) -> 'EFFECT':
        return self.__effect

    def __str__(self):
        return f"( forall ({' '.join(map(str, self.__variables))}) {self.__effect} )"


class ConditionalEffect(AbstractEffect):
    """ Conditional effect.

    eff_conditional : '(' 'when' gd effect ')';

    :param gd: condition
    :param effect: effect
    """
    def __init__(self, gd: GD, effect: 'EFFECT'):
        self.__gd = gd
        self.__effect = effect

    @property
    def condition(self) -> GD:
        return self.__gd

    @property
    def effect(self) -> 'EFFECT':
        return self.__effect

    def __str__(self):
        return f"( when {self.__gd} {self.__effect} )"


class PEffect(AbstractEffect):
    """ Numeric effect.

    p_effect : '(' assign_op f_head f_exp ')';

    :param op: assignement operator (assign, scale-down, scale-up, increase, decrease)
    :param predicate: predicate
    :param expression:
    """
    def __init__(self, op: str, predicate: AtomicFormula, expression: FluentExpression):
        self.__op = op
        self.__predicate = predicate
        self.__expression = expression

    def __str__(self):
        return f"({self.__op} {self.__predicate} {self.__expression})"


EFFECT = Union[LITERAL, AbstractEffect]