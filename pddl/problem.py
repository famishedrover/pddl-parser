""" Description of a PDDL problem. """

from typing import List, Union

from .formula import AtomicFormula, NotFormula, AndFormula
from .domain import Constant
from .belief import UnknownLiteral, OrBelief, OneOfBelief
from .hierarchy import Method

Literal = Union[AtomicFormula,NotFormula]
InitElement = Union[AtomicFormula,NotFormula,UnknownLiteral,OrBelief,OneOfBelief]
Goal = Union[AtomicFormula, NotFormula, AndFormula]

class Problem(object):
    """ PDDL problem

    :param name: problem name
    :param domain: domain name
    :param init: initial state
    :param goal: goal state
    :param htn: HTN task to decompose
    :param requirements: list of requirements
    :param objects: list of objects of the problem
    """
    def __init__(self,
                 name: str,
                 domain: str,
                 init: List[InitElement],
                 goal: Goal = None,
                 htn: Method = None,
                 requirements: List[str] = [],
                 objects: List[Constant] = []):
        self.__name = name
        self.__domain = domain
        self.__init = init
        self.__goal = goal
        self.__htn = htn
        self.__requirements = requirements
        self.__objects = objects

    @property
    def name(self) -> str:
        return self.__name

    @property
    def domain(self) -> str:
        return self.__domain

    @property
    def init(self) -> List[InitElement]:
        return self.__init

    @property
    def goal(self) -> Goal:
        return self.__goal

    @property
    def requirements(self) -> List[str]:
        return self.__requirements

    @property
    def objects(self) -> List[Constant]:
        return self.__objects

    @property
    def htn(self) -> Method:
        return self.__htn
