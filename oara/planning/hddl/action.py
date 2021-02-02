from typing import List, Optional, Dict, Iterator

from .types import TypedVariable, TypedObject
from .gd import GD, EmptyGD
from .effect import EFFECT, EmptyEffect


class Action:
    """PDDL action.

    :param name: action name
    :param parameters: action parameters
    :param precondition: action precondition
    :param effect: action state effect
    """

    def __init__(self, name: str,
                 parameters: List[TypedVariable] = (),
                 precondition: GD = EmptyGD(),
                 effect: EFFECT = EmptyEffect(),
                 #observe: AtomicFormula = None
                 ):
        self.__name = name
        self.__parameters = parameters
        self.__precondition = precondition
        self.__effect = effect
        #self.__observe = observe

    @property
    def name(self) -> str:
        """Action name."""
        return self.__name

    @property
    def parameters(self) -> List[TypedVariable]:
        """Action parameters."""
        return self.__parameters

    @property
    def precondition(self) -> GD:
        """Action precondition."""
        return self.__precondition

    @property
    def effect(self) -> EFFECT:
        """Action effect."""
        return self.__effect

    def __str__(self) -> str:
        return f"""
    (:action {self.__name}
        :parameters ({' '.join(map(str, self.__parameters))})
        :precondition {self.__precondition}
        :effect {self.__effect}
    )"""

    def __eq__(self, other) -> bool:
        return self.__name == other.__name

    def __hash__(self):
        return self.__name.__hash__()

    def ground(self, assignment: Dict[str, str]) -> 'Action':
        params = []
        for p in self.parameters:
            if p.name in assignment:
                params.append(TypedObject(assignment[p.name], p.types))
            else:
                params.append(p)
        return Action(self.name,
            parameters=params,
            precondition=self.precondition.ground(assignment)
            )
