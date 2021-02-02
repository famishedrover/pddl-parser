from typing import List, Union, Dict


class AtomicFormula:
    """
    (<predicate> <args*>)
    """
    def __init__(self, predicate: str, arguments: List[str]):
        self.__predicate = predicate
        self.__arguments = arguments

    @property
    def predicate(self) -> str:
        return self.__predicate

    @property
    def arguments(self) -> List[str]:
        return self.__arguments

    def __str__(self) -> str:
        return f"({self.__predicate} {' '.join(self.__arguments)})"

    def __eq__(self, other: 'AtomicFormula'):
        return self.__predicate == other.__predicate and self.__arguments == other.__arguments

    def __hash__(self):
        return self.__str__().__hash__()

    def ground(self, assignment: Dict[str, str]):
        self.__arguments = map(assignment.get, self.__arguments, self.__arguments)


class NegFormula:
    """
    (not <formula>)
    """
    def __init__(self, formula: AtomicFormula):
        self.__formula = formula

    @property
    def formula(self) -> AtomicFormula:
        return self.__formula

    def __str__(self) -> str:
        return f"(not {self.__formula})"

    def ground(self, assignment: Dict[str, str]):
        self.__formula.ground(assignment)


LITERAL = Union[AtomicFormula, NegFormula]
