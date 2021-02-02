from typing import List, Optional, Dict, Iterator

from .types import Type, TypedObject
from .predicate import Predicate
from .function import Function
from .action import Action
from .hierarchy import Task, Method


class HDDLDomain:
    """PDDL domain.

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
                 constants: List[TypedObject] = [],
                 predicates: List[Predicate] = [],
                 functions: List[Function] = [],
                 actions: List[Action] = [],
                 tasks: List[Task] = [],
                 methods: List[Method] = []
                 ):
        self.__name = name
        self.__requirements = requirements
        self.__types = types
        self.__constants = constants
        self.__predicates = predicates
        self.__functions = functions
        self.__actions = actions
        self.__tasks = tasks
        self.__methods = methods

    @property
    def name(self) -> str:
        """Domain name."""
        return self.__name

    @property
    def types(self) -> List[Type]:
        """Domain types."""
        return self.__types

    @property
    def requirements(self) -> List[str]:
        """Domain requirements."""
        return self.__requirements

    @property
    def constants(self) -> List[TypedObject]:
        """Domain constants."""
        return self.__constants

    @property
    def predicates(self) -> List[Predicate]:
        """Domain predicates."""
        return self.__predicates

    @property
    def functions(self) -> List[Function]:
        """Domain functions."""
        return self.__functions

    @property
    def actions(self) -> List[Action]:
        """Domain actions."""
        return self.__actions

    @property
    def tasks(self) -> List[Task]:
        """Domain tasks."""
        return self.__tasks

    @property
    def methods(self) -> List[Method]:
        """Domain methods."""
        return self.__methods

    def __str__(self) -> str:
        nltab = '\n\t'
        return f"""(define (domain {self.__name}))
    (:requirements {' '.join(self.__requirements)})
    (:types 
        {nltab.join(map(str, self.__types))}
    )
    (:constants 
        {nltab.join(map(str, self.__constants))}
    )
    (:predicates
        {nltab.join(map(str, self.__predicates))}
    )
    (:functions
        {nltab.join(map(str, self.__functions))}
    )
    {nltab.join(map(str, self.__tasks))}
    {nltab.join(map(str, self.__methods))}
    {nltab.join(map(str, self.__actions))}
)"""