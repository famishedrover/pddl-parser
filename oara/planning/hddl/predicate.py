from typing import List, Iterator, Dict

from .types import TypedVariable
from .formula import AtomicFormula


class Predicate:

    """PDDL predicate.

    :param name: predicate name
    :param variables: predicate variables
    """

    def __init__(self, name: str, variables: List[TypedVariable] = []):
        self.__name = name
        self.__variables = variables

    @property
    def name(self) -> str:
        """Get name."""
        return self.__name

    @property
    def variables(self) -> List[TypedVariable]:
        """Get variables."""
        return self.__variables

    def __str__(self):
        return f"({self.__name} {' '.join(map(str, self.__variables))})"

    def __lt__(self, other: 'Predicate'):
        return self.__name < other.__name

    def __eq__(self, other) -> bool:
        return self.__name == other.__name

    def __hash__(self):
        return self.__name.__hash__()

    def ground(self, assignment: Dict[str, str]) -> AtomicFormula:
        """Ground the predicate.

        :param assignment: variables assignment function
        """
        return AtomicFormula(self.__name, [assignment[v.name] for v in self.__variables])