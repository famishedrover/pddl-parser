"""PDDL Parser visitor."""

from collections import defaultdict
import itertools

from .parser.antlrHDDLVisitor import antlrHDDLVisitor as AbstractPDDLVisitor
from .parser.antlrHDDLParser import antlrHDDLParser

from .domain import Domain, Type, Constant, Variable, Predicate, Action
from .variable import Function
from .problem import Problem
from .formula import AtomicFormula, NotFormula, AndFormula
from .formula import ForallFormula, WhenEffect, FluentEffect
from .belief import UnknownLiteral, OrBelief, OneOfBelief
from .hierarchy import Task, Method, TaskNetwork
from .expression import Number, Function, UnaryOp, MultiOp
from .logger import LOGGER


class PDDLVisitor(AbstractPDDLVisitor):
    """PDDL Visitor implementation."""

    def __init__(self):
        """Construct the Visitor."""
        AbstractPDDLVisitor.__init__(self)
        self.task_index = 0

    def index_task(self):
        """Compute task index if tasks not indexed in input file."""
        i = self.task_index
        self.task_index += 1
        return i

    def visitHddl_file(self, ctx:antlrHDDLParser.Hddl_fileContext):
        if ctx.domain():
            return self.visit(ctx.domain())
        elif ctx.problem():
            return self.visit(ctx.problem())
        else:
            raise AttributeError(ctx)

    def visitDomain(self, ctx: antlrHDDLParser.DomainContext):
        name = self.visit(ctx.domain_symbol())
        requirements = self.visit(ctx.require_def())
        types = []
        if ctx.type_def():
            types = self.visit(ctx.type_def())
        constants = []
        if ctx.const_def():
            constants = self.visit(ctx.const_def())
        actions = [self.visit(a) for a in ctx.action_def()]
        tasks = []
        if ctx.comp_task_def():
            tasks = [self.visit(a) for a in ctx.comp_task_def()]
        methods = []
        if ctx.method_def():
            methods = [self.visit(a) for a in ctx.method_def()]
        predicates = []
        if ctx.predicates_def():
            predicates = self.visit(ctx.predicates_def())
        functions = []
        if ctx.funtions_def():
            functions = self.visit(ctx.funtions_def())
        return Domain(name=name,
                      requirements=requirements,
                      types=types,
                      constants=constants,
                      predicates=predicates,
                      functions=functions,
                      actions=actions,
                      tasks=tasks,
                      methods=methods)

    def visitDomain_symbol(self, ctx:antlrHDDLParser.Domain_symbolContext):
        return ctx.NAME()

    def visitRequire_def(self, ctx:antlrHDDLParser.Require_defContext):
        return self.visit(ctx.require_defs())

    def visitRequire_defs(self, ctx:antlrHDDLParser.Require_defsContext):
        return [n.symbol.text for n in ctx.REQUIRE_NAME()]

    def visitType_def(self, ctx:antlrHDDLParser.Type_defContext):
        return self.visit(ctx.type_def_list())

    def visitType_def_list(self, ctx:antlrHDDLParser.Type_def_listContext):
        if ctx.NAME():
            return [Type(n.symbol.text, 'object') for n in ctx.NAME()]
        # subtypes def
        if ctx.var_type():
            supertype = self.visit(ctx.var_type())
        else:
            supertype = 'object'
        new_types = []
        if ctx.new_types():
            for t in self.visit(ctx.new_types()):
                new_types.append(Type(t, supertype))
        if ctx.type_def_list():
            new_types += self.visit(ctx.type_def_list())
        return new_types

    def visitVar_type(self, ctx:antlrHDDLParser.Var_typeContext):
        if ctx.NAME():
            return ctx.NAME().symbol.text
        else:
            raise AttributeError(ctx)

    def visitNew_types(self, ctx:antlrHDDLParser.New_typesContext):
        return [n.symbol.text for n in ctx.NAME()]

    def visitConst_def(self, ctx:antlrHDDLParser.Const_defContext):
        return self.visit(ctx.typed_obj_list())

    def visitTyped_obj_list(self, ctx:antlrHDDLParser.Typed_obj_listContext):
        return [v for o in ctx.typed_objs() for v in self.visit(o)]

    def visitTyped_objs(self, ctx:antlrHDDLParser.Typed_objsContext):
        if ctx.var_type():
            supertype = self.visit(ctx.var_type())
        else:
            supertype = 'object'
        new_consts = []
        for c in ctx.new_consts():
            t = self.visit(c)
            new_consts.append(Constant(t, supertype))
        return new_consts

    def visitNew_consts(self, ctx:antlrHDDLParser.New_constsContext):
        return ctx.NAME().symbol.text

    def visitAction_def(self, ctx:antlrHDDLParser.Action_defContext):
        return self.visit(ctx.task_def())

    def visitTask_def(self, ctx:antlrHDDLParser.Task_defContext):
        name = self.visit(ctx.task_symbol())
        parameters = self.visit(ctx.typed_var_list())
        precondition = self.visit(ctx.gd()) if ctx.gd() else []
        effect = self.visit(ctx.effect()) if ctx.effect() else []
        return Action(name,
                      parameters=parameters,
                      precondition=precondition,
                      effect=effect)
                      #observe=(self.visit(ctx.observe)
                      #         if ctx.observe else None))

    def visitTask_symbol(self, ctx:antlrHDDLParser.Task_symbolContext):
        return ctx.NAME().symbol.text

    def visitTyped_var_list(self, ctx:antlrHDDLParser.Typed_var_listContext):
        return [v for t in ctx.typed_vars() for v in self.visit(t)]

    def visitTyped_vars(self, ctx:antlrHDDLParser.Typed_varsContext):
        if ctx.var_type():
            supertype = self.visit(ctx.var_type())
        else:
            supertype = 'object'
        new_vars = []
        for v in ctx.VAR_NAME():
            new_vars.append(Variable(v.symbol.text, supertype))
        return new_vars

    def visitEffect(self, ctx:antlrHDDLParser.EffectContext):
        if ctx.eff_empty(): return self.visit(ctx.eff_empty())
        if ctx.eff_conjunction(): return self.visit(ctx.eff_conjunction())
        if ctx.eff_universal(): return self.visit(ctx.eff_universal())
        if ctx.eff_conditional(): return self.visit(ctx.eff_conditional())
        if ctx.literal(): return self.visit(ctx.literal())
        if ctx.p_effect(): return self.visit(ctx.p_effect())

    def visitEff_empty(self, ctx:antlrHDDLParser.Eff_emptyContext):
        return AndFormula([])

    def visitEff_conjunction(self, ctx:antlrHDDLParser.Eff_conjunctionContext):
        return AndFormula([self.visit(e) for e in ctx.effect()])

    def visitEff_universal(self, ctx:antlrHDDLParser.Eff_universalContext):
        return ForallFormula(self.visit(ctx.typed_var_list()), 
                             self.visit(ctx.effect))

    def visitEff_conditional(self, ctx:antlrHDDLParser.Eff_conditionalContext):
        return WhenEffect(self.visit(ctx.gd()),
                          self.visit(ctx.effect()))

    def visitNeg_atomic_formula(self, ctx:antlrHDDLParser.Neg_atomic_formulaContext):
        return NotFormula(self.visit(ctx.atomic_formula()))

    def visitAtomic_formula(self, ctx:antlrHDDLParser.Atomic_formulaContext):
        return AtomicFormula(self.visit(ctx.predicate()),
                             [self.visit(t) for t in ctx.var_or_const()])

    def visitPredicate(self, ctx:antlrHDDLParser.PredicateContext):
        return ctx.NAME().symbol.text

    def visitVar_or_const(self, ctx:antlrHDDLParser.Var_or_constContext):
        if ctx.NAME():
            return ctx.NAME().symbol.text
        elif ctx.VAR_NAME():
            return ctx.VAR_NAME().symbol.text
        else:
            raise AttributeError(ctx)

    def visitP_effect(self, ctx:antlrHDDLParser.P_effectContext):
        return FluentEffect(self.visit(ctx.assign_op()),
                            self.visit(ctx.f_head()),
                            self.visit(ctx.f_exp()))

    def visitAssign_op(self, ctx:antlrHDDLParser.Assign_opContext):
        return ctx.start.text

    def visitF_head(self, ctx:antlrHDDLParser.F_headContext):
        return AtomicFormula(self.visit(ctx.func_symbol()),
                             [self.visit(t) for t in ctx.term()])

    def visitFunc_symbol(self, ctx:antlrHDDLParser.Func_symbolContext):
        return ctx.NAME().symbol.text

    def visitTerm(self, ctx:antlrHDDLParser.TermContext):
        if ctx.NAME():
            return ctx.NAME().symbol.text
        elif ctx.VAR_NAME():
            return ctx.VAR_NAME().symbol.text
        elif ctx.functionterm():
            return self.visit(ctx.functionterm())
        else:
            raise AttributeError(ctx)

    def visitFunctionterm(self, ctx:antlrHDDLParser.FunctiontermContext):
        return AtomicFormula(self.visit(ctx.func_symbol()),
                             [self.visit(t) for t in ctx.term()])

    def visitComp_task_def(self, ctx:antlrHDDLParser.Comp_task_defContext):
        a = self.visit(ctx.task_def())
        return Task(a.name, a.parameters)

    def visitMethod_def(self, ctx:antlrHDDLParser.Method_defContext):
        name = self.visit(ctx.method_symbol())
        task = AtomicFormula(self.visit(ctx.task_symbol()), 
                             [self.visit(t) for t in ctx.var_or_const()])
        parameters = self.visit(ctx.typed_var_list()) if ctx.typed_var_list() else []
        precondition = self.visit(ctx.gd()) if ctx.gd() else AndFormula([])
        effect = self.visit(ctx.effect()) if ctx.effect() else AndFormula([])
        tn = self.visit(ctx.tasknetwork_def())
        return Method(name, task,
                      parameters=parameters,
                      precondition=precondition,
                      effect=effect,
                      tn=tn)

    def visitMethod_symbol(self, ctx:antlrHDDLParser.Method_symbolContext):
        return ctx.NAME().symbol.text

    def visitTasknetwork_def(self, ctx:antlrHDDLParser.Tasknetwork_defContext):
        subtasks = self.visit(ctx.subtask_defs())
        ordering = defaultdict(list)
        if ':ordered' in ctx.start.text:
            subtasks_i, subtasks_j = itertools.tee(subtasks)
            next(subtasks_j, None)
            for s_i, s_j in zip(subtasks_i, subtasks_j):
                ordering[s_i[0]].append(s_j[0])
        elif ctx.ordering_defs():
            order = self.visit(ctx.ordering_defs())
            for head, tail in order:
                for task in tail:
                    ordering[head].append(task)
        constraints = self.visit(ctx.constraint_defs()) if ctx.constraint_defs() else []
        causal_links = self.visit(ctx.causallink_defs()) if ctx.causallink_defs() else []
        return TaskNetwork(subtasks, ordering, constraints, causal_links)

    def visitSubtask_defs(self, ctx:antlrHDDLParser.Subtask_defsContext):
        return [self.visit(t) for t in ctx.subtask_def()]

    def visitSubtask_def(self, ctx:antlrHDDLParser.Subtask_defContext):
        id = self.visit(ctx.subtask_id()) if ctx.subtask_id() else f"task{self.index_task()}"
        return (id, AtomicFormula(self.visit(ctx.task_symbol()),
                                  [self.visit(t) for t in ctx.var_or_const()]))

    def visitOrdering_defs(self, ctx:antlrHDDLParser.Ordering_defsContext):
        return [self.visit(o) for o in ctx.ordering_def()]

    def visitOrdering_def(self, ctx:antlrHDDLParser.Ordering_defContext):
        return (self.visit(i) for i in ctx.subtask_id())

    def visitPredicates_def(self, ctx:antlrHDDLParser.Predicates_defContext):
        return [self.visit(p) for p in ctx.atomic_formula_skeleton()]

    def visitAtomic_formula_skeleton(self, ctx:antlrHDDLParser.Atomic_formula_skeletonContext):
        return Predicate(self.visit(ctx.predicate()),
                         self.visit(ctx.typed_var_list()))

    def visitFuntions_def(self, ctx:antlrHDDLParser.Funtions_defContext):
        functions = []
        for f in ctx.atomic_formula_skeleton():
            p = self.visit(f)
            type = self.visit(ctx.var_type()) if ctx.var_type() else 'number'
            functions.append(Function(p.name, p.variables, type))
        return functions

    ############# PROBLEM ##################################################

    def visitProblem(self, ctx:antlrHDDLParser.ProblemContext):
        objects = self.visit(ctx.p_object_declaration()) if ctx.p_object_declaration() else []
        requirements = self.visit(ctx.require_def()) if ctx.require_def() else []
        init = self.visit(ctx.p_init())
        goal = self.visit(ctx.p_goal()) if ctx.p_goal() else AndFormula([])
        htn = self.visit(ctx.p_htn()) if ctx.p_htn() else None
        # constraints
        metric = self.visit(ctx.metric_spec()) if ctx.metric_spec() else None
        return Problem(ctx.NAME(0),
                 ctx.NAME(0), # domain
                 init=init,
                 goal=goal,
                 htn=htn,
                 requirements=requirements,
                 objects=objects,
                 metric=metric)

    def visitP_object_declaration(self, ctx:antlrHDDLParser.P_object_declarationContext):
        return self.visit(ctx.typed_obj_list())

    def visitP_init(self, ctx:antlrHDDLParser.P_initContext):
        return [self.visit(i) for i in ctx.init_el()]

    def visitNum_init(self, ctx:antlrHDDLParser.Num_initContext):
        return Predicate('=', [self.visit(ctx.f_head()), ctx.NUMBER()])

    def visitP_htn(self, ctx:antlrHDDLParser.P_htnContext):
        params = self.visit(ctx.typed_var_list()) if ctx.typed_var_list() else []
        return Method('__top_method__', 
                      AtomicFormula('__top__', params),
                      tn=self.visit(ctx.tasknetwork_def()))

    def visitMetric_spec(self, ctx:antlrHDDLParser.Metric_specContext):
        return (self.visit(ctx.optimization()), self.visit(ctx.ground_f_exp()))

    def visitOptimization(self, ctx:antlrHDDLParser.OptimizationContext):
        return ctx.start.text

    def visitGround_f_exp(self, ctx:antlrHDDLParser.Ground_f_expContext):
        if ctx.NUMBER():
            return Number(ctx.NUMBER())
        elif ctx.start.text == 'total-time':
            return Function('total-time')
        elif ctx.func_symbol():
            return Function(self.visit(ctx.func_symbol()), [n.symbol.text for n in ctx.NAME()])
        elif ctx.bin_op():
            return MultiOp(self.visit(ctx.bin_op()), [self.visit(e) for e in ctx.ground_f_exp()])
        elif ctx.multi_op():
            return MultiOp(self.visit(ctx.multi_op()), [self.visit(e) for e in ctx.ground_f_exp()])
        else: # should be '( - <expr> )'
            return UnaryOp('-', self.visit(ctx.ground_f_exp()))