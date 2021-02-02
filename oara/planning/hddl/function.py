from typing import List

from ..exceptions import NotSupported
from .types import TypedVariable


class Function:

    """PDDL function.

    :param name: function name
    :param variables: function variables
    """

    def __init__(self, name: str, 
                variables: List[TypedVariable] = [], 
                type: str = 'number'):
        self.__name = name
        self.__variables = variables
        if isinstance(type, list):
            if len(type) > 1:
                raise NotSupported(f"multiple types {type} for function {name}")
            elif len(type) == 0:
                self.__type = 'number'
        else:
            self.__type = type

    @property
    def name(self) -> str:
        """Get name."""
        return self.__name

    @property
    def variables(self) -> List[TypedVariable]:
        """Get variables."""
        return self.__variables

    @property
    def type(self) -> str:
        """Get type."""
        return self.__type

    def __str__(self):
        return f"( ({self.__name} {' '.join(map(str, self.__variables))}) - {self.__type} )"

    def __lt__(self, other: 'Function'):
        return self.__name < other.__name

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self):
        return self.__name.__hash__()
