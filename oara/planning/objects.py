from typing import Dict, List, Set, Iterator, Tuple, Callable, Iterable
import networkx
import networkx.drawing.nx_pydot as pydot
import itertools
from collections import defaultdict

from .logger import LOGGER
from .hddl.problem import HDDLProblem
from .hddl.domain import HDDLDomain
from .hddl.types import Type, TypedVariable


class Objects:
    """Objects of the problem.

    Objects are sorted by (super) types.

    :param problem: the PDDL problem
    :param domain: the PDDL domain
    """
    def __init__(self, problem: HDDLProblem, domain: HDDLDomain):
        
        self.__domain = domain
        self.__problem = problem

        self.__subtypes_closure(domain.types)
        LOGGER.info("Types: %d", len(self.__types_hierarchy))
        LOGGER.debug("Types: %s", self.__types_hierarchy.nodes)

        self.__objects_per_type = defaultdict(set)
        objects = set()
        for obj in domain.constants:
            for t in obj.types:
                self.__objects_per_type[t].add(obj.name)
            objects.add(obj.name)
        for obj in problem.objects:
            for t in obj.types:
                self.__objects_per_type[t].add(obj.name)
            objects.add(obj.name)
        for t, subt in self.__types_subtypes.items():
            for st in subt:
                self.__objects_per_type[t] |= self.__objects_per_type[st]
        LOGGER.info("Objects: %d", len(objects))
        LOGGER.debug("Objects: %s", objects)
        LOGGER.debug("Objects per type:")
        for typ, objs in self.__objects_per_type.items():
            LOGGER.debug('- %s: %s', typ, objs)

        self.__objects = list(objects)
        for typ, objs in self.__objects_per_type.items():
            self.__objects_per_type[typ] = list(sorted(objs))

    def __iter__(self):
        return self.__objects.__iter__()

    '''
    @property
    def types(self) -> Iterator[str]:
        """Get all types."""
        return self.__objects_per_type.keys()

    def per_type(self, objtype: str = 'object') -> Iterator[str]:
        """Get all objects of a given type.

        :param objtype: the given type
        """
        return self.__objects_per_type[objtype].__iter__()
    '''

    def __subtypes_closure(self, types: List[Type]):
        """Computes the transitive closure of types hierarchy."""
        types_hierarchy = networkx.DiGraph()
        for typ in types:
            types_hierarchy.add_edge(typ.type, typ.name)
            types_hierarchy.add_edge('object', typ.type)
        self.__types_hierarchy = networkx.transitive_closure(types_hierarchy)
        graph = self.__types_hierarchy
        self.__types_subtypes = {n: frozenset(graph.successors(n)) for n in graph}

    def write_dot(self, filename: str, with_objects: bool = False):
        graph = networkx.DiGraph()
        for typ in self.__domain.types:
            graph.add_edge(typ.type, typ.name)
            graph.add_edge('object', typ.type)
        
        if with_objects:
            for obj in self.__domain.constants:
                for t in obj.types:
                    graph.add_edge(t, obj, style='dashed')
            for obj in self.__problem.objects:
                for t in obj.types:
                    graph.add_edge(t, obj, style='dashed')
        
        pydot.write_dot(graph, filename)
        
    def iter_objects(self, variables: Iterable[TypedVariable]):
                     #objects: Callable[[str], List[str]],
                     #assignment: Dict[str, str]) -> Iterable[List[Tuple[str, List[str]]]]:
        var_assign = []
        if not variables:
            return [[('?','?')]]
        for var in variables:
            #if var.name in assignment:
            #    assigns = [(var.name, assignment[var.name])]
            #else:
            for t in var.types:
                assigns = itertools.product([var.name], self.__objects_per_type[t])
                var_assign.append(assigns)
        return itertools.product(*var_assign)
