from typing import List, Union, Optional

from ..exceptions import AlreadyDefined

from .types import TypedObject, TypedVariable
from .formula import AtomicFormula, NegFormula, LITERAL
from .expression import EqualityExp
from .gd import GD, EmptyGD
from .hierarchy import TaskNetwork
from .metric import Metric

INIT_EL = Union[LITERAL, EqualityExp]


class HDDLProblem:
    """PDDL problem.

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
                 requirements: List[str] = [],
                 objects: List[TypedObject] = [],
                 init: List[INIT_EL] = [],
                 goal: GD = EmptyGD(),
                 htn: Optional[TaskNetwork] = None,
                 htn_parameters: List[TypedVariable] = [],
                 metric: Optional[Metric] = None):
        self.__name = name
        self.__domain_name = domain
        self.__init = init
        self.__goal = goal
        self.__htn = htn
        self.__htn_parameters = htn_parameters
        self.__requirements = requirements
        self.__objects = objects
        self.__metric = metric

    @property
    def name(self) -> str:
        """Problem name."""
        return self.__name

    @property
    def domain(self) -> str:
        """Domain name."""
        return self.__domain_name

    @property
    def requirements(self) -> List[str]:
        """Problem requirements."""
        return self.__requirements

    @property
    def objects(self) -> List[TypedObject]:
        """Problem objects."""
        return self.__objects

    @property
    def init(self) -> List[INIT_EL]:
        return self.__init

    @property
    def goal(self) -> GD:
        return self.__goal

    @property
    def htn(self) -> Optional[TaskNetwork]:
        return self.__htn

    @property
    def htn_parameters(self) -> List[TypedVariable]:
        return self.__htn_parameters

    #def merge(self, other: 'Problem') -> 'Problem':
    #    return Problem(
    #        self.name, self.domain,
    #        self.init + other.init,
    #        AndFormula([self.goal, other.goal]),
    #        self.htn if self.htn else other.htn,
    #        self.requirements + other.requirements,
    #        self.objects + other.objects,
    #        self.metric if self.metric else other.metric
    #    )

    def __str__(self) -> str:
        nltab = '\n\t'
        return f"""(define (problem {self.__name})
    (:domain {self.__domain_name})
    {f"(:requirements {' '.join(self.__requirements)})" if self.__requirements else ''}
    (:objects 
        {nltab.join(map(str, self.__objects))}
    )
    (:htn 
        {':parameters' if self.__htn_parameters else ''} {' '.join(map(str, self.__htn_parameters))}
        {self.__htn}
    )
    (:init 
        {nltab.join(map(str, self.__init))}
    )
    {f"(:goal {self.__goal})" if self.goal else ''}
    {self.__metric if self.__metric else ''}
)"""
