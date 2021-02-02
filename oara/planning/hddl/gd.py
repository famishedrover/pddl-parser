from typing import List, Union, Dict
from abc import ABC, abstractmethod

from .formula import AtomicFormula
from .types import TypedVariable


class AbstractGD(ABC):
    """ Abstract Goal Description

    gd : gd_empty | atomic_formula | gd_negation | gd_implication | gd_conjuction 
        | gd_disjuction | gd_existential | gd_universal | gd_equality_constraint
        | gd_ltl_at_end | gd_ltl_always | gd_ltl_sometime | gd_ltl_at_most_once 
        | gd_ltl_sometime_after | gd_ltl_sometime_before
        | gd_preference;
    """
    @abstractmethod
    def ground(self, assignment: Dict[str, str]) -> 'GD':
        pass


class EmptyGD(AbstractGD):
    """ Empty Goal."""
    def __str__(self) -> str:
        return f"()"
    def ground(self, assignment: Dict[str, str]) -> 'EmptyGD':
        return EmptyGD()

class NegationGD(AbstractGD):
    """ Negation Goal.
    
    gd_negation : '(' 'not' gd ')';

    :param gd: goal.
    """
    def __init__(self, gd: 'GD'):
        self.__gd = gd

    @property
    def gd(self) -> 'GD':
        return self.__gd

    def __str__(self) -> str:
        return f"(not {self.__gd})"

    def ground(self, assignment: Dict[str, str]) -> 'NegationGD':
        return NegationGD(self.__gd.ground(assignment))


class ImplicationGD(AbstractGD):
    """ Implication Goal.
    
    gd_implication : '(' 'imply' gd gd ')';

    :param left: left goal.
    :param right: right goal.
    """
    def __init__(self, left: 'GD', right: 'GD'):
        self.__left = left
        self.__right = right

    def __str__(self) -> str:
        return f"(imply {self.__left} {self.__right})"

    def ground(self, assignment: Dict[str, str]) -> 'ImplicationGD':
        return ImplicationGD(self.__left.ground(assignment),
                             self.__right.ground(assignment))


class ConjunctionGD(AbstractGD):
    """ Conjunction of Goals.
    
    gd_conjuction : '(' 'and' gd+ ')';

    :param gds: goals.
    """
    def __init__(self, gds: List['GD']):
        self.__gds = gds

    @property
    def gds(self) -> List['GD']:
        return self.__gds

    def __str__(self) -> str:
        return f"(and {' '.join(map(str, self.__gds))})"

    def ground(self, assignment: Dict[str, str]) -> 'ConjunctionGD':
        return ConjunctionGD(map(assignment.get, self.__gds, self.__gds))


class DisjunctionGD(AbstractGD):
    """ Disjunction of Goals.
    
    gd_disjuction : '(' 'or' gd+ ')';

    :param gds: goals.
    """
    def __init__(self, gds: List['GD']):
        self.__gds = gds

    def __str__(self) -> str:
        return f"(or {' '.join(map(str, self.__gds))})"

    def ground(self, assignment: Dict[str, str]) -> 'DisjunctionGD':
        return DisjunctionGD(map(assignment.get, self.__gds, self.__gds))


class ExistentialGD(AbstractGD):
    """ Existential Goal.
    
    gd_existential : '(' 'exists' '(' typed_var_list ')' gd ')';

    :param variables: existential variables.
    :param gd: goal.
    """
    def __init__(self, variables: List[TypedVariable], gd: 'GD'):
        self.__variables = variables
        self.__gd = gd

    def __str__(self) -> str:
        return f"(exists ({' '.join(self.__variables)}) {self.__gd})"


class UniversalGD(AbstractGD):
    """ Universal Goal.
    
    gd_universal : '(' 'forall' '(' typed_var_list ')' gd ')';

    :param variables: universal variables.
    :param gd: goal.
    """
    def __init__(self, variables: List[TypedVariable], gd: 'GD'):
        self.__variables = variables
        self.__gd = gd

    def __str__(self) -> str:
        return f"(forall ({' '.join(self.__variables)}) {self.__gd})"


class EqualityGD(AbstractGD, AtomicFormula):
    """ Equality Constraint.
    
    gd_equality_constraint : equallity var_or_const var_or_const ')';
    equallity : '(' '=' | '(=';

    :param left: left var.
    :param right: right var.
    """
    def __init__(self, left: str, right: str):
        AtomicFormula.__init__(self, '=', [left, right])

    def ground(self, assignment: Dict[str, str]) -> 'EqualityGD':
        return AtomicFormula.ground(self, assignment)


GD = Union[AbstractGD, AtomicFormula]
