from typing import Tuple, Iterator, List, Dict, Any, Callable, Set
from collections import defaultdict

from .exceptions import NotSupported

from .hddl import HDDLDomain, HDDLProblem
from .hddl.effect import EFFECT, ConjunctionEffect, ConditionalEffect, UniversalEffect
from .hddl.formula import AtomicFormula, NegFormula
from .hddl.gd import GD, NegationGD, ImplicationGD, ConjunctionGD, DisjunctionGD, ExistentialGD, UniversalGD, EqualityGD

from .objects import Objects
from .atoms import Atoms
from .logic import Expression, Not, And, FalseExpr, TrueExpr, Atom

from .logger import LOGGER


class Literals:
    def __init__(self, domain: HDDLDomain, problem: HDDLProblem, 
                 objects: Objects,
                 equality: bool = False):
        # Build all Atoms
        atoms_per_predicate = defaultdict(set)
        for predicate in sorted(domain.predicates):
            for args in objects.iter_objects(predicate.variables):
                atom = Atoms.atom(predicate.ground(dict(args)))
                atoms_per_predicate[predicate.name].add(atom)
        LOGGER.info("Predicates: %d", len(atoms_per_predicate))
        LOGGER.info("Atoms: %d", len(Atoms.atoms()))
        # Fluents
        self.__fluents = set()
        for action in domain.actions:
            expr = self.__build_effect_expression(action.effect, objects)
            pos, neg = expr.support
            self.__fluents |= pos
            self.__fluents |= neg
        LOGGER.info("Fluents: %d", len(self.__fluents))
        LOGGER.debug("Fluents: %s", self.__fluents)
        self.__rigid = set(
            pred.name for pred in domain.predicates) - self.__fluents
        if equality:
            self.__rigid.add('=')
        LOGGER.info("Rigid relations: %d", len(self.__rigid))
        LOGGER.debug("Rigid relations: %s", self.__rigid)
        # Rigid Literals
        rigid_atoms = set(a for p, atoms in atoms_per_predicate.items()
                            for a in atoms
                            if p in self.__rigid)
        LOGGER.info("Rigid atoms: %d", len(rigid_atoms))
        LOGGER.debug("Rigid atoms: %s", rigid_atoms)
        pb_init = set(Atoms.atom(lit) for lit in problem.init)
        LOGGER.debug("Problem init state: %s", pb_init)
        if equality:
            equals = set(Atoms.atom(AtomicFormula('=', [o, o])) for o in objects)
            diffs = set(Atoms.atom(AtomicFormula('=', [o, u]))
                        for o in objects for u in objects if u != o)
        else:
            equals = set()
            diffs = set()
        rigid_atoms |= equals | diffs
        self.__rigid_literals = (((pb_init | equals) & rigid_atoms),
                                 (rigid_atoms - pb_init) - equals)
        LOGGER.info("Rigid literals: %d", sum(map(len, self.__rigid_literals)))
        LOGGER.debug("Rigid literals: %s", self.__rigid_literals)
        # Init State
        self.__init_literals = (
            pb_init - self.__rigid_literals[0]), (Atoms.atoms() - rigid_atoms - pb_init)
        LOGGER.info("Init state literals: %d", sum(
            map(len, self.__init_literals)))
        LOGGER.debug("Init state literals: %s", self.__init_literals)
        # Goal state
        '''
        self.__goal_literals = self.__build_gd_expression(problem.goal, objects).support
        LOGGER.info("Goal state literals: %d", sum(
            map(len, self.__goal_literals)))
        LOGGER.debug("Goal state literals: %s", self.__goal_literals)
        '''
        
    def __build_effect_expression(self, effect: EFFECT, objects: Objects) -> Expression:
        if isinstance(effect, AtomicFormula):
            return Atom(effect.predicate)
        if isinstance(effect, NegFormula):
            return Not(self.__build_effect_expression(effect.formula, objects))
        if isinstance(effect, ConjunctionEffect):
            return And(*[self.__build_effect_expression(f, objects)
                         for f in effect.effects])

        if isinstance(effect, ConditionalEffect):
            raise NotSupported(effect)
        if isinstance(effect, UniversalEffect):
            raise NotSupported(effect)

        return TrueExpr()

    def __build_gd_expression(self, gd: GD, objects: Objects) -> Expression:
        if isinstance(gd, AtomicFormula):
            return Atom(gd.predicate)
        if isinstance(gd, NegationGD):
            return Not(self.__build_gd_expression(gd.gd, objects))
        if isinstance(gd, ConjunctionGD):
            return And(*[self.__build_gd_expression(f, objects)
                         for f in gd.gds])

        if isinstance(gd, ImplicationGD):
            raise NotSupported(gd)
        if isinstance(gd, UniversalGD):
            raise NotSupported(gd)
        if isinstance(gd, EqualityGD):
            raise NotSupported(gd)
        if isinstance(gd, DisjunctionGD):
            raise NotSupported(gd)
        if isinstance(gd, ExistentialGD):
            raise NotSupported(gd)
        
        return TrueExpr()

    '''
    @property
    def rigid_relations(self) -> Set[str]:
        return self.__rigid

    @property
    def rigid_literals(self) -> Tuple[Set[int], Set[int]]:
        return self.__rigid_literals

    @property
    def varying_relations(self) -> Set[str]:
        return self.__fluents

    @property
    def varying_literals(self) -> Set[int]:
        a, b = self.__init_literals
        return a | b

    @property
    def init(self) -> Tuple[Set[int], Set[int]]:
        return self.__init_literals

    def __assign(self, args: List[str], assignment: Dict[str, str], 
                 complete: bool = True) -> List[str]:
        result = []
        for a in args:
            if a in assignment:
                result.append(assignment[a])
            elif complete and a[0] == '?':
                # a is a variable
                raise KeyError()
            else:
                result.append(a)
        return result

    def build(self, formula: GOAL,
              assignment: Dict[str, str],
              objects: Objects) -> Expression:
        def atom_factory(x, *args):
            a, _ = Atoms.atom(x, *args)
            return a
        return self.__build_expression(formula, assignment, objects, atom_factory)

    def build_partial(self, formula: GOAL,
                      assignment: Dict[str, str],
                      objects: Objects,
                      atom_factory: Callable[[List[str]], Any]) -> Expression:
        return self.__build_expression(formula, assignment, objects, atom_factory)

    def extract(self, fun: Callable[[Any, GOAL], Any], formula: GOAL) -> Any:
        def list_extract(fun, formula, result):
            if isinstance(formula, pddl.AtomicFormula):
                result = fun(result, formula)
            if isinstance(formula, pddl.NotFormula):
                result = list_extract(fun, formula.formula, result)
            if isinstance(formula, pddl.AndFormula):
                for f in formula.formulas:
                    result = list_extract(fun, f, result)
            return result
        return list_extract(fun, formula, [])
    '''