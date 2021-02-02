"""Classes related to the Domain types."""

from typing import List, Union

from ..exceptions import NotSupported


class Type:
    """PDDL type.

    (`name` - `supertype`)
    """

    def __init__(self, name: str, supertype: Union[str, List] = 'object'):
        """
        :param name: type name
        :param type: supertype name
        """
        self.__name = name
        if isinstance(supertype, list):
            if len(supertype) > 1:
                raise NotSupported(f"multiple supertypes {supertype} for type {name}")
            elif len(supertype) == 0:
                self.__type = 'object'
        else:
            self.__type = supertype

    @property
    def name(self) -> str:
        """Get type name."""
        return self.__name

    @property
    def type(self) -> str:
        """Get super type."""
        return self.__type

    def __str__(self) -> str:
        if self.type:
            return "{} - {}".format(self.name, self.type)
        return self.name

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self):
        return self.__name.__hash__()


class TypedVariable:
    """ PDDL typed variable. 

    (`name` - `type`)
    (`name` - ( either `type1` `type2`)
    """

    def __init__(self, name: str, types: List[str] = ['object']):
        """
        :param name: variable name
        :param types: variables types
        """
        self.__name = name
        if isinstance(types, list):
            self.__types = types
        else:
            self.__types = [types]

    @property
    def name(self) -> str:
        """Get variable name."""
        return self.__name

    @property
    def types(self) -> str:
        """Get variable types."""
        return self.__types

    def __str__(self) -> str:
        if len(self.types) == 1:
            return f"{self.name} - {self.types[0]}"
        else:
            return f"{self.name} - ( either {' '.join(self.types)} )"

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self):
        return self.__name.__hash__()


class TypedObject:
    """ PDDL typed object. 

    (`name` - `type`)
    (`name` - ( either `type1` `type2`)
    """

    def __init__(self, name: str, types: List[str] = ['object']):
        """
        :param name: object name
        :param types: object types
        """
        self.__name = name
        if isinstance(types, list):
            self.__types = types
        else:
            self.__types = [types]

    @property
    def name(self) -> str:
        """Get object name."""
        return self.__name

    @property
    def types(self) -> str:
        """Get object types."""
        return self.__types

    def __str__(self) -> str:
        if len(self.types) == 1:
            return f"{self.name} - {self.types[0]}"
        else:
            return f"{self.name} - ( either {' '.join(self.types)} )"

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self):
        return self.__name.__hash__()
