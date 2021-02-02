#!/usr/bin/env python3
"""OARA Planning library entry point."""

import argparse
import logging
import sys

from .logger import LOGGER, setup_logging
from .hddl.parsing import parse_domain, parse_problem, parse
from .hddl import HDDLProblem, HDDLDomain, Task
from .objects import Objects
from .literals import Literals

def main():
    """Implement main function."""
    parser = argparse.ArgumentParser(prog='oara.planning')
    # common args
    parser.add_argument("hddl", help="HDDL domain/problem files",
                        nargs='+', type=str)
    parser.add_argument("-d", "--debug", help="Activate debug logs",
                        action='store_const', dest="loglevel",
                        const=logging.DEBUG, default=logging.WARNING)
    parser.add_argument("-v", "--verbose", help="Activate verbose logs",
                        action='store_const', dest="loglevel",
                        const=logging.INFO, default=logging.WARNING)
    parser.add_argument('-p', '--pprint',
                        help='pretty print the parsed model',
                        action='store_true')
    # options
    parser.add_argument('--parse', help="parse (only) and show parsing result", action='store_true')
    parser.add_argument('--ground', help="ground the model -- requires both a domain and problem files", action='store_true')
    
    #              
    args = parser.parse_args()
    setup_logging(args.loglevel)

    # parsing
    if args.parse:
        print("-"*80)
        for hddl in args.hddl:
            print(parse(hddl, file_stream=True))
            print("-"*80)
        return

    # grounding
    if args.ground:
        if len(args.hddl) != 2:
            LOGGER.error(f"Grounding needs exactly one problem and one domain files. {len(args.hddl)} files provided.")
            return

        domain = parse(args.hddl[0], file_stream=True)
        problem = parse(args.hddl[1], file_stream=True)

        if isinstance(domain, HDDLDomain) and isinstance(problem, HDDLProblem):
            LOGGER.info(f"parsed domain {domain.name} and problem {problem.name}")
        elif isinstance(domain, HDDLProblem) and isinstance(problem, HDDLDomain):
            tmp = domain
            domain = problem
            problem = tmp
            LOGGER.info(f"parsed domain {domain.name} and problem {problem.name}")
        else:
            LOGGER.error("Grounding needs exactly one problem and one domain files; you passed either two domains or two problems!")
            return

        objects = Objects(problem, domain)
        objects.write_dot(f'{problem.name}-objects.dot', with_objects=True)
        literals = Literals(domain, problem, objects, True)


        if problem.htn is not None:
            top_task = Task('__top__', problem.htn_parameters)
            for assignment in objects.iter_objects(top_task.parameters):
                print(assignment)
                t = top_task.ground(dict(assignment))
                print(t)

        '''
        # Goal task
        if problem.htn:
            LOGGER.info("HTN problem")
            tasks = list(domain.tasks) + [pddl.Task('__top')]
            methods = list(domain.methods) + [problem.htn]
        else:
            tasks = domain.tasks
            methods = domain.methods

        # Actions grounding
        LOGGER.info("PDDL actions: %d", len(domain.actions))
        LOGGER.info("Possible action groundings: %d",
                    self.__nb_grounded_operators(domain.actions))
        ground = self.__ground_operator
        tic = time.process_time()
        self.__grounded_actions = dict()
        for action in domain.actions:
            groundings = list(ground(action, GroundedAction, dict()))
            LOGGER.debug("operator %s has %d groundings", action.name, len(groundings))
            self.__grounded_actions.update({str(a): a for a in groundings})
        toc = time.process_time()
        LOGGER.info("action grounding duration: %.3fs", (toc - tic))
        LOGGER.info("Grounded actions: %d", len(self.__grounded_actions))

        # H-Add
        tic = time.process_time()
        self.__hadd = HAdd(self.__grounded_actions.values(),
                           self.__literals.init[0],
                           self.__literals.varying_literals
                           )
        toc = time.process_time()
        LOGGER.info("hadd duration: %.3fs", (toc - tic))
        if output is not None:
            self.__hadd.write_dot(f"{output}hadd-graph.dot")
        LOGGER.info("Reachable actions: %d", sum(
            1 for a in self.__grounded_actions if not math.isinf(self.__hadd(a))))

        # Methods grounding
        LOGGER.info("PDDL methods: %d", len(methods))
        #LOGGER.info("Possible method groundings: %d",
        #            self.__nb_grounded_operators(methods))
        ground = self.__ground_operator
        tic = time.process_time()
        self.__grounded_methods = dict()
        for op in methods:
            groundings = list(ground(op, GroundedMethod, dict()))
            LOGGER.debug("operator %s has %d groundings",
                         op.name, len(groundings))
            self.__grounded_methods.update({str(a): a for a in groundings})
        toc = time.process_time()
        LOGGER.info("method grounding duration: %.3fs", (toc - tic))
        LOGGER.info("Grounded methods: %d", len(self.__grounded_methods))

        # Tasks grounding
        LOGGER.info("PDDL tasks: %d", len(tasks))
        LOGGER.info("Possible task groundings: %d",
                    self.__nb_grounded_operators(tasks))
        ground = self.__ground_operator
        tic = time.process_time()
        self.__grounded_tasks = dict()
        for op in tasks:
            groundings = list(ground(op, GroundedTask, dict()))
            LOGGER.debug("operator %s has %d groundings",
                         op.name, len(groundings))
            self.__grounded_tasks.update({str(a): a for a in groundings})
        toc = time.process_time()
        LOGGER.info("task grounding duration: %.3fs", (toc - tic))
        LOGGER.info("Grounded tasks: %d", len(self.__grounded_tasks))

        # Lifted TDG
        # TODO: move to tdg.py
        tic = time.process_time()
        lifted_tdg = networkx.DiGraph()
        for m in methods:
            lifted_tdg.add_edge(m.task.name, m.name)
            for (_, t) in m.network.subtasks:
                lifted_tdg.add_edge(m.name, t.name)
        toc = time.process_time()
        LOGGER.info("lifted TDG duration: %.3fs", (toc - tic))
        if output is not None:
            pydot.write_dot(lifted_tdg, f"{output}tdg-lifted.dot")

        if tdg_cycles:
            try:
                cycle = networkx.find_cycle(lifted_tdg)
                LOGGER.info("Domain is recursive")
                LOGGER.debug("Found cycle in lifted TDG: %s", cycle)
            except networkx.NetworkXNoCycle:
                pass
        # TODO: we can first filter on the lifted TDG! even including action not reachable in delete-relaxation

        # TDG
        tic = time.process_time()
        self.__tdg = TaskDecompositionGraph(
            self.__grounded_actions, self.__grounded_methods, self.__grounded_tasks, 
            self.__hadd)
        toc = time.process_time()
        LOGGER.info("initial TDG duration: %.3fs", (toc - tic))
        LOGGER.info("TDG initial: %d", len(self.__tdg))
        if output is not None:
            self.__tdg.write_dot(f"{output}tdg-initial.dot")
        # Remove useless nodes
        tic = time.process_time()
        if filter_relaxed:
            self.__tdg.remove_useless(
                (a for a in self.__grounded_actions if math.isinf(self.__hadd(a))))
        else:
            self.__tdg.remove_useless(())
        toc = time.process_time()
        LOGGER.info("TDG filtering duration: %.3fs", (toc - tic))
        LOGGER.info("TDG minimal: %d", len(self.__tdg))
        if output is not None:
            self.__tdg.write_dot(f"{output}tdg-minimal.dot")
        # Keep only HTN decomposition
        if problem.htn and pure_htn:
            tic = time.process_time()
            self.__tdg.htn('(__top )')
            toc = time.process_time()
            LOGGER.info("TDG HTN filtering duration: %.3fs", (toc - tic))
            LOGGER.info("TDG HTN: %d", len(self.__tdg))
            if output is not None:
                self.__tdg.write_dot(f"{output}tdg-htn.dot")
        if tdg_cycles:
            LOGGER.info("TDG cycles: %d", len(list(self.__tdg.cycles)))
        tic = time.process_time()
        self.__tdg.compute_heuristics()
        toc = time.process_time()
        LOGGER.info("TDG heuristics duration: %.3fs", (toc - tic))
        if output is not None:
            self.__tdg.write_dot(f"{output}tdg-htn.dot")

        self.__recursive = bool(self.__tdg.has_cycles())
        if self.__recursive:
            LOGGER.info("Problem is recursive")

        # Mutex a.k.a. Position/Motion Fluents
        self.__mutex = defaultdict(frozenset)
        if mutex:
            tic = time.process_time()
            for pred in self.__literals.varying_relations:
                lits = set(l[0] for l in Atoms.atoms_of(pred))
                if self.__is_unique(lits):
                    LOGGER.info("Motion predicate: %s", pred)
                    for l in lits:
                        self.__mutex[l] = frozenset(lits - {l})
            toc = time.process_time()
            LOGGER.info("Mutex computation duration: %.3fs", (toc - tic))
            LOGGER.debug("Mutex: %s", self.__mutex)
        '''

    '''
    def __ground_operator(self, op: Any, gop: type,
                        assignments: Dict[str, str]) -> Iterator[Type[GroundedOperator]]:
        """Ground an operator."""
        try:
            vars_in_rigid = set(self.__literals.extract(self.__fun_extract_rigid, op.precondition))
        except AttributeError:
            vars_in_rigid = set()
        LOGGER.debug("%s: %d parameters; %d used in rigid relations", op.name, len(op.parameters), len(vars_in_rigid))

        rigid_params = [p for p in op.parameters if p.name in vars_in_rigid] if op.parameters else []

        build = self.__literals.build_partial
        if rigid_params:
            for rigid_assign in iter_objects(rigid_params, self.__objects.per_type, assignments):
                expr = build(op.precondition, dict(rigid_assign), self.__objects, self.__fun_format_rigid)
                LOGGER.debug("%s partial rigid pre: %s", op.name, expr)
                expr = expr.simplify(*self.__literals.rigid_literals)
                LOGGER.debug("%s partial rigid simplified pre: %s", op.name, expr)
                if isinstance(expr, FalseExpr):
                    LOGGER.debug("droping operator %s for impossible rigid grounding", op.name)
                    continue
                for assignment in iter_objects(op.parameters, self.__objects.per_type, rigid_assign):
                    try:
                        yield gop(op, dict(assignment), literals=self.__literals, objects=self.__objects)
                    except GroundingImpossibleError as ex:
                        LOGGER.debug("droping operator %s : %s [%s]", op.name, ex.message, ex.__class__.__name__)
                        pass
        else:
            for assignment in iter_objects(op.parameters, self.__objects.per_type, assignments):
                try:
                    LOGGER.debug(assignment)
                    yield gop(op, dict(assignment), literals=self.__literals, objects=self.__objects)
                except GroundingImpossibleError as ex:
                    LOGGER.debug(
                        "droping operator %s : %s [%s]", op.name, ex.message, ex.__class__.__name__)
    '''

if __name__ == '__main__':
    main()
