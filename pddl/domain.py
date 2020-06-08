"""
Classes related to the Domain description.
"""

from typing import List, Union, Optional
from .formula import *
from .variable import Type, Constant, Variable, Predicate
from .hierarchy import Task, Method

class Action(object):
    """ PDDL action

    :param name: action name
    :param parameters: action parameters
    :param precondition: action precondition
    :param effect: action state effect
    :param observe: action observation effect
    """
    def __init__(self, name: str,
                 parameters: List[Variable] = [],
                 precondition: Union[AtomicFormula,NotFormula,AndFormula] = None,
                 effect: Union[AtomicFormula,NotFormula,AndFormula,WhenEffect] = None,
                 observe: AtomicFormula = None
                 ):
        self.__name = name
        self.__parameters = parameters
        self.__precondition = precondition
        self.__effect = effect
        self.__observe = observe

    @property
    def name(self) -> str:
        return self.__name

    @property
    def parameters(self) -> List[Variable]:
        return self.__parameters

    @property
    def precondition(self) -> Union[AtomicFormula,NotFormula,AndFormula]:
        return self.__precondition

    @property
    def effect(self) -> Union[AtomicFormula,NotFormula,AndFormula,WhenEffect]:
        return self.__effect

    @property
    def observe(self) -> Optional[AtomicFormula]:
        return self.__observe

class Domain(object):
    """ PDDL domain

    :param name: domain name
    :param requirements: list of domain requirements
    :param types: domain types
    :param constants: domain constants
    :param predicates: domain predicates
    :param actions: domain actions
    :param tasks: domain tasks
    :param methods: domain methods
    """
    def __init__(self, name: str,
                 requirements: List[str] = [],
                 types: List[Type] = [],
                 constants: List[Constant] = [],
                 predicates: List[Predicate] = [],
                 actions: List[Action] = [],
                 tasks: List[Task] = [],
                 methods: List[Method] = []
                 ):
        self.__name = name
        self.__requirements = requirements
        self.__types = types
        self.__constants = constants
        self.__predicates = predicates
        self.__actions = actions
        self.__tasks = tasks
        self.__methods = methods

    @property
    def name(self) -> str:
        return self.__name

    @property
    def requirements(self) -> List[str]:
        return self.__requirements

    @property
    def types(self) -> List[Type]:
        return self.__types

    @property
    def constants(self) -> List[Constant]:
        return self.__constants

    @property
    def predicates(self) -> List[Predicate]:
        return self.__predicates

    @property
    def actions(self) -> List[Action]:
        return self.__actions

    @property
    def tasks(self) -> List[Task]:
        return self.__tasks

    @property
    def methods(self) -> List[Method]:
        return self.__methods
