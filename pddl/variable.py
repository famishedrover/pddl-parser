"""
Classes related to the Domain variables and types.
"""

from typing import List, Union, Optional
from .formula import *

class Type(object):
    """PDDL type

    :param name: type name
    :param type: supertype name
    """
    def __init__(self, name: str, type: str = 'object'):
        self.__name = name
        self.__type = type

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> str:
        return self.__type

    def __str__(self):
        if self.type:
            return "{} - {}".format(self.name, self.type)
        else:
            return self.name

class Constant(Type):
    """ PDDL constant """
    pass

class Variable(Type):
    """ Variable used in predicates and similar constructs """
    pass

class Predicate(object):
    """ PDDL predicate

    :param name: predicate name
    :param variables: predicate variables
    """
    def __init__(self, name: str, variables: List[Variable] = []):
        self.__name = name
        self.__variables = variables

    @property
    def name(self) -> str:
        return self.__name

    @property
    def variables(self) -> List[Variable]:
        return self.__variables
