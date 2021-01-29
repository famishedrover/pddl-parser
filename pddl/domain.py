"""Classes related to the Domain description."""

from typing import List, Optional, Dict, Iterator
from .formula import AtomicFormula, AndFormula, WhenEffect
from .variable import Type, Constant, Variable, Predicate
from .hierarchy import Task, Method


class Action:

    """PDDL action.

    :param name: action name
    :param parameters: action parameters
    :param precondition: action precondition
    :param effect: action state effect
    :param observe: action observation effect
    """

    def __init__(self, name: str,
                 parameters: List[Variable] = (),
                 precondition: AndFormula = None,
                 effect: AndFormula = None,
                 observe: AtomicFormula = None):
        self.__name = name
        self.__parameters = parameters
        self.__precondition = precondition
        self.__effect = effect
        self.__observe = observe

    @property
    def name(self) -> str:
        """Get name."""
        return self.__name

    @property
    def parameters(self) -> List[Variable]:
        """Get parameters."""
        return self.__parameters

    @property
    def precondition(self) -> AndFormula:
        """Get precondition."""
        return self.__precondition

    @property
    def effect(self) -> AndFormula:
        """Get effect."""
        return self.__effect

    @property
    def observe(self) -> Optional[AtomicFormula]:
        """Get observation effect."""
        return self.__observe

    def __str__(self) -> str:
        return f"""
    (:action {self.name}
        :parameters ({' '.join(map(str, self.parameters))})
        :precondition {self.precondition}
        :effect {self.effect}
    )"""

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self):
        return self.__name.__hash__()

class Domain:

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
                 constants: List[Constant] = [],
                 predicates: List[Predicate] = [],
                 functions = [],
                 actions: List[Action] = [],
                 tasks: List[Task] = [],
                 methods: List[Method] = []):
        self.__name = name
        self.__requirements = list(set(requirements))
        self.__types = list(set(types))
        self.__constants = list(set(constants))
        self.__predicates = list(set(predicates))
        self.__actions = list(set(actions))
        self.__tasks = list(set(tasks))
        self.__methods = list(set(methods))
        self.functions = list(set(functions))

    def merge(self, other: 'Domain') -> 'Domain':
        return Domain(self.name,
            requirements=self.requirements + other.requirements,
            types=self.types + other.types,
            constants=self.constants + other.constants,
            predicates=self.predicates + other.predicates,
            functions=self.functions + other.functions,
            actions=self.actions + other.actions,
            tasks=self.tasks + other.tasks,
            methods=self.methods + other.methods
        )

    @property
    def name(self) -> str:
        """Get name."""
        return self.__name

    @property
    def requirements(self) -> List[str]:
        """Get list of requirements."""
        return self.__requirements

    @property
    def types(self) -> List[Type]:
        """Get set of types."""
        return self.__types

    @property
    def constants(self) -> List[Constant]:
        """Get set of constants."""
        return self.__constants

    @property
    def predicates(self) -> List[Predicate]:
        """Get predicates."""
        return self.__predicates

    @property
    def actions(self) -> List[Action]:
        """Get actions."""
        return self.__actions

    @property
    def tasks(self) -> List[Task]:
        """Get tasks."""
        return self.__tasks

    @property
    def methods(self) -> List[Method]:
        """Get methods."""
        return self.__methods

    def __str__(self) -> str:
        nl = '\n'
        return f"""(define (domain {self.name}))
    (:requirements {' '.join(self.requirements)})
    (:types {nl.join(map(str, self.types))})
)"""