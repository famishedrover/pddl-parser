from typing import Tuple, Iterator, List, Dict
from collections import defaultdict
from itertools import count

from .logger import LOGGER
from .hddl.formula import AtomicFormula


class Atoms:
    __atoms = defaultdict(dict)
    __predicates = defaultdict(dict)
    __counter = count(0)

    @classmethod
    def atoms(cls):
        return cls.__predicates.keys()

    @classmethod
    def atom(cls, formula: AtomicFormula) -> int:
        if formula not in cls.__atoms:
            c = next(cls.__counter)
            cls.__atoms[formula] = c
            cls.__predicates[c] = formula
            LOGGER.debug(f"atom {c}: {formula}")
            return c
        else:
            return cls.__atoms[formula]

    @classmethod
    def atom_to_predicate(cls, atom: int) -> AtomicFormula:
        return cls.__predicates[atom]
