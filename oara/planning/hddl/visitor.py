"""PDDL Parser visitor."""

from collections import defaultdict
import itertools

from .parser.antlrHDDLVisitor import antlrHDDLVisitor as AbstractPDDLVisitor
from .parser.antlrHDDLParser import antlrHDDLParser

from ..exceptions import NotSupported

from .domain import HDDLDomain
from .types import Type, TypedObject, TypedVariable
from .predicate import Predicate
from .function import Function
from .action import Action
from .formula import AtomicFormula, NegFormula
from .effect import EmptyEffect, ConditionalEffect, ConjunctionEffect, UniversalEffect, PEffect
from .expression import Number, OppositeExp, AdditionExp, MultiplicationExp, SubstractionExp, DivisionExp, EqualityExp, FunctionExp
from .gd import EmptyGD, ConjunctionGD, DisjunctionGD, ImplicationGD, NegationGD, UniversalGD, ExistentialGD, EqualityGD
from .hierarchy import Task, Method, Subtask, Ordering, TaskNetwork, OrderedTaskNetwork
from .metric import Metric
from .problem import HDDLProblem


class PDDLVisitor(AbstractPDDLVisitor):
    """PDDL Visitor implementation."""

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
        
        supertypes = self.visit(ctx.var_type()) if ctx.var_type() else 'object'
        new_types = []
        if ctx.new_types():
            for t in self.visit(ctx.new_types()):
                new_types.append(Type(t, supertypes))
        if ctx.type_def_list():
            new_types += self.visit(ctx.type_def_list())
        return new_types

    def visitNew_types(self, ctx:antlrHDDLParser.New_typesContext):
        return [n.symbol.text for n in ctx.NAME()]

    def visitVar_type(self, ctx:antlrHDDLParser.Var_typeContext):
        if ctx.NAME():
            return ctx.NAME().symbol.text
        else:
            return [self.visit(t) for t in ctx.var_type()]

    def visitConst_def(self, ctx:antlrHDDLParser.Const_defContext):
        return self.visit(ctx.typed_obj_list())

    def visitTyped_obj_list(self, ctx:antlrHDDLParser.Typed_obj_listContext):
        return [v for o in ctx.typed_objs() for v in self.visit(o)]

    def visitTyped_objs(self, ctx:antlrHDDLParser.Typed_objsContext):
        supertype = self.visit(ctx.var_type()) if ctx.var_type() else 'object'
        new_consts = []
        for c in ctx.new_consts():
            t = self.visit(c)
            new_consts.append(TypedObject(t, supertype))
        return new_consts

    def visitNew_consts(self, ctx:antlrHDDLParser.New_constsContext):
        return ctx.NAME().symbol.text

    def visitPredicates_def(self, ctx:antlrHDDLParser.Predicates_defContext):
        return [self.visit(p) for p in ctx.atomic_formula_skeleton()]

    def visitAtomic_formula_skeleton(self, ctx:antlrHDDLParser.Atomic_formula_skeletonContext):
        return Predicate(self.visit(ctx.predicate()),
                         self.visit(ctx.typed_var_list()))

    def visitPredicate(self, ctx:antlrHDDLParser.PredicateContext):
        return ctx.NAME().symbol.text

    def visitTyped_var_list(self, ctx:antlrHDDLParser.Typed_var_listContext):
        return [v for t in ctx.typed_vars() for v in self.visit(t)]

    def visitTyped_vars(self, ctx:antlrHDDLParser.Typed_varsContext):
        supertype = self.visit(ctx.var_type()) if ctx.var_type() else 'object'
        return [TypedVariable(v.symbol.text, supertype) for v in ctx.VAR_NAME()]

    def visitFuntions_def(self, ctx:antlrHDDLParser.Funtions_defContext):
        functions = []
        for f in ctx.atomic_formula_skeleton():
            p = self.visit(f)
            type = self.visit(ctx.var_type()) if ctx.var_type() else 'number'
            functions.append(Function(p.name, p.variables, type))
        return functions

    def visitAction_def(self, ctx:antlrHDDLParser.Action_defContext):
        return self.visit(ctx.task_def())

    def visitTask_symbol(self, ctx:antlrHDDLParser.Task_symbolContext):
        return ctx.NAME().symbol.text

    def visitTask_def(self, ctx:antlrHDDLParser.Task_defContext):
        name = self.visit(ctx.task_symbol())
        parameters = self.visit(ctx.typed_var_list()) if ctx.typed_var_list() else []
        precondition = self.visit(ctx.gd()) if ctx.gd() else EmptyGD()
        effect = self.visit(ctx.effect()) if ctx.effect() else EmptyEffect()
        return Action(name,
                      parameters=parameters,
                      precondition=precondition,
                      effect=effect)
                      #observe=(self.visit(ctx.observe)
                      #         if ctx.observe else None))

    def visitEffect(self, ctx:antlrHDDLParser.EffectContext):
        if ctx.eff_empty(): return self.visit(ctx.eff_empty())
        if ctx.eff_conjunction(): return self.visit(ctx.eff_conjunction())
        if ctx.eff_universal(): return self.visit(ctx.eff_universal())
        if ctx.eff_conditional(): return self.visit(ctx.eff_conditional())
        if ctx.literal(): return self.visit(ctx.literal())
        if ctx.p_effect(): return self.visit(ctx.p_effect())

    def visitEff_empty(self, ctx:antlrHDDLParser.Eff_emptyContext):
        return EmptyEffect()

    def visitEff_conjunction(self, ctx:antlrHDDLParser.Eff_conjunctionContext):
        return ConjunctionEffect([self.visit(e) for e in ctx.effect()])

    def visitEff_universal(self, ctx:antlrHDDLParser.Eff_universalContext):
        return UniversalEffect(self.visit(ctx.typed_var_list()), 
                             self.visit(ctx.effect))

    def visitLiteral(self, ctx:antlrHDDLParser.LiteralContext):
        if ctx.atomic_formula():
            return self.visit(ctx.atomic_formula())
        elif ctx.neg_atomic_formula():
            return self.visit(ctx.neg_atomic_formula())
        else:
            raise AttributeError(ctx)

    def visitAtomic_formula(self, ctx:antlrHDDLParser.Atomic_formulaContext):
        return AtomicFormula(self.visit(ctx.predicate()),
                             [self.visit(t) for t in ctx.var_or_const()])

    def visitNeg_atomic_formula(self, ctx:antlrHDDLParser.Neg_atomic_formulaContext):
        return NegFormula(self.visit(ctx.atomic_formula()))

    def visitVar_or_const(self, ctx:antlrHDDLParser.Var_or_constContext):
        if ctx.NAME():
            return ctx.NAME().symbol.text
        elif ctx.VAR_NAME():
            return ctx.VAR_NAME().symbol.text
        else:
            raise AttributeError(ctx)

    def visitEff_conditional(self, ctx:antlrHDDLParser.Eff_conditionalContext):
        return ConditionalEffect(self.visit(ctx.gd()),
                          self.visit(ctx.effect()))

    def visitAssign_op(self, ctx:antlrHDDLParser.Assign_opContext):
        return ctx.start.text

    def visitFunc_symbol(self, ctx:antlrHDDLParser.Func_symbolContext):
        return ctx.NAME().symbol.text

    def visitF_head(self, ctx:antlrHDDLParser.F_headContext):
        return FunctionExp(self.visit(ctx.func_symbol()),
                               [self.visit(t) for t in ctx.term()])

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
        return FunctionExp(self.visit(ctx.func_symbol()),
                                [self.visit(t) for t in ctx.term()])

    def visitP_effect(self, ctx:antlrHDDLParser.P_effectContext):
        return PEffect(self.visit(ctx.assign_op()),
                        self.visit(ctx.f_head()),
                        self.visit(ctx.f_exp()))

    def visitF_exp(self, ctx:antlrHDDLParser.F_expContext):
        if ctx.NUMBER():
            return Number(ctx.NUMBER())
        elif ctx.f_head():
            return self.visit(ctx.f_head())
        elif ctx.bin_op():
            op = self.visit(ctx.bin_op())
            if op == '+': return AdditionExp([self.visit(e) for e in ctx.f_exp()])
            elif op == '*': return MultiplicationExp([self.visit(e) for e in ctx.f_exp()])
            elif op == '-': return SubstractionExp([self.visit(e) for e in ctx.f_exp()])
            elif op == '/': return DivisionExp([self.visit(e) for e in ctx.f_exp()])
            else: raise AttributeError(ctx.bin_op())
        elif ctx.multi_op():
            op = self.visit(ctx.multi_op())
            if op == '+': return AdditionExp([self.visit(e) for e in ctx.f_exp()])
            elif op == '*': return MultiplicationExp([self.visit(e) for e in ctx.f_exp()])
            else: raise AttributeError(ctx.multi_op())
        else: # should be '( - <expr> )'
            return OppositeExp(self.visit(ctx.f_exp()))

    def visitBin_op(self, ctx:antlrHDDLParser.Bin_opContext):
        if ctx.multi_op(): return self.visit(ctx.multi_op())
        else: return ctx.start.text

    def visitMulti_op(self, ctx:antlrHDDLParser.Multi_opContext):
        return ctx.start.text

    def visitGd_empty(self, ctx:antlrHDDLParser.Gd_emptyContext):
        return EmptyGD()

    def visitGd_conjuction(self, ctx:antlrHDDLParser.Gd_conjuctionContext):
        return ConjunctionGD([self.visit(g) for g in ctx.gd()])

    def visitGd_disjuction(self, ctx:antlrHDDLParser.Gd_disjuctionContext):
        return DisjunctionGD([self.visit(g) for g in ctx.gd()])

    def visitGd_negation(self, ctx:antlrHDDLParser.Gd_negationContext):
        return NegationGD(self.visit(ctx.gd()))

    def visitGd_implication(self, ctx:antlrHDDLParser.Gd_implicationContext):
        return ImplicationGD(*[self.visit(g) for g in ctx.gd()])

    def visitGd_existential(self, ctx:antlrHDDLParser.Gd_existentialContext):
        return ExistentialGD(self.visit(ctx.typed_var_list()), self.visit(ctx.gd()))

    def visitGd_universal(self, ctx:antlrHDDLParser.Gd_universalContext):
        return UniversalGD(self.visit(ctx.typed_var_list()), self.visit(ctx.gd()))

    def visitGd_equality_constraint(self, ctx:antlrHDDLParser.Gd_equality_constraintContext):
        return EqualityGD(*[self.visit(v) for v in ctx.var_or_const()])

    def visitGd(self, ctx:antlrHDDLParser.GdContext):
        return self.visitChildren(ctx)

    def visitComp_task_def(self, ctx:antlrHDDLParser.Comp_task_defContext):
        a = self.visit(ctx.task_def())
        a.__class__ = Task
        return a

    def visitMethod_symbol(self, ctx:antlrHDDLParser.Method_symbolContext):
        return ctx.NAME().symbol.text

    def visitMethod_def(self, ctx:antlrHDDLParser.Method_defContext):
        name = self.visit(ctx.method_symbol())
        task = AtomicFormula(self.visit(ctx.task_symbol()), 
                             [self.visit(t) for t in ctx.var_or_const()])
        parameters = self.visit(ctx.typed_var_list()) if ctx.typed_var_list() else []
        precondition = self.visit(ctx.gd()) if ctx.gd() else EmptyGD()
        effect = self.visit(ctx.effect()) if ctx.effect() else EmptyEffect()
        tn = self.visit(ctx.tasknetwork_def())
        return Method(name, 
                      task,
                      parameters=parameters,
                      precondition=precondition,
                      effect=effect,
                      tn=tn)

    def visitSubtask_defs(self, ctx:antlrHDDLParser.Subtask_defsContext):
        return [self.visit(t) for t in ctx.subtask_def()]

    def visitSubtask_def(self, ctx:antlrHDDLParser.Subtask_defContext):
        id = self.visit(ctx.subtask_id()) if ctx.subtask_id() else None
        return Subtask(id, self.visit(ctx.task_symbol()), [self.visit(t) for t in ctx.var_or_const()])

    def visitSubtask_id(self, ctx:antlrHDDLParser.Subtask_idContext):
        return ctx.NAME().symbol.text

    def visitOrdering_defs(self, ctx:antlrHDDLParser.Ordering_defsContext):
        return [self.visit(o) for o in ctx.ordering_def()]

    def visitOrdering_def(self, ctx:antlrHDDLParser.Ordering_defContext):
        return Ordering(*[self.visit(i) for i in ctx.subtask_id()])

    def visitTasknetwork_def(self, ctx:antlrHDDLParser.Tasknetwork_defContext):
        subtasks = self.visit(ctx.subtask_defs())
        constraints = self.visit(ctx.constraint_defs()) if ctx.constraint_defs() else []
        causal_links = self.visit(ctx.causallink_defs()) if ctx.causallink_defs() else []
        if ':ordered' in ctx.start.text:
            return OrderedTaskNetwork(subtasks)
        else:
            ordering = self.visit(ctx.ordering_defs()) if ctx.ordering_defs() else []
            return TaskNetwork(subtasks, ordering)

    def visitHddl_file(self, ctx:antlrHDDLParser.Hddl_fileContext):
        if ctx.domain():
            return self.visit(ctx.domain())
        elif ctx.problem():
            return self.visit(ctx.problem())
        else:
            raise AttributeError(ctx)

    def visitDomain(self, ctx: antlrHDDLParser.DomainContext):
        name = self.visit(ctx.domain_symbol())
        requirements = self.visit(ctx.require_def()) if ctx.require_def() else []
        types = self.visit(ctx.type_def()) if ctx.type_def() else []
        constants = self.visit(ctx.const_def()) if ctx.const_def() else []
        predicates = self.visit(ctx.predicates_def()) if ctx.predicates_def() else []
        functions = self.visit(ctx.funtions_def()) if ctx.funtions_def() else []
        actions = [self.visit(a) for a in ctx.action_def()]
        tasks = [self.visit(a) for a in ctx.comp_task_def()] if ctx.comp_task_def() else []
        methods = [self.visit(a) for a in ctx.method_def()] if ctx.method_def() else []
        return HDDLDomain(name=name,
                      requirements=requirements,
                      types=types,
                      constants=constants,
                      predicates=predicates,
                      functions=functions,
                      actions=actions,
                      tasks=tasks,
                      methods=methods
                      )

    #############################################################################
    #############################################################################
    #############################################################################
    #############################################################################
    #############################################################################

    def visitP_object_declaration(self, ctx:antlrHDDLParser.P_object_declarationContext):
        return self.visit(ctx.typed_obj_list())

    def visitP_init(self, ctx:antlrHDDLParser.P_initContext):
        return [self.visit(i) for i in ctx.init_el()]

    def visitInit_el(self, ctx:antlrHDDLParser.Init_elContext):
        if ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.num_init():
            return self.visit(ctx.num_init())
        else:
            raise AttributeError(ctx)

    def visitNum_init(self, ctx:antlrHDDLParser.Num_initContext):
        return EqualityExp(self.visit(ctx.f_head()), Number(ctx.NUMBER()))

    def visitP_goal(self, ctx:antlrHDDLParser.P_goalContext):
        return self.visit(ctx.gd())

    def visitMetric_spec(self, ctx:antlrHDDLParser.Metric_specContext):
        return Metric(self.visit(ctx.optimization()), self.visit(ctx.ground_f_exp()))

    def visitOptimization(self, ctx:antlrHDDLParser.OptimizationContext):
        return ctx.start.text

    def visitGround_f_exp(self, ctx:antlrHDDLParser.Ground_f_expContext):
        if ctx.NUMBER():
            return Number(ctx.NUMBER())
        elif ctx.func_symbol():
            return FunctionExp(self.visit(ctx.func_symbol()), [n.symbol.text for n in ctx.NAME()])
        elif 'total-time' in ctx.start.text:
            return FunctionExp('total-time')
        elif ctx.bin_op():
            op = self.visit(ctx.bin_op())
            if op == '+': return AdditionExp([self.visit(e) for e in ctx.ground_f_exp()])
            elif op == '*': return MultiplicationExp([self.visit(e) for e in ctx.ground_f_exp()])
            elif op == '-': return SubstractionExp([self.visit(e) for e in ctx.ground_f_exp()])
            elif op == '/': return DivisionExp([self.visit(e) for e in ctx.ground_f_exp()])
            else: raise AttributeError(ctx.bin_op())
        elif ctx.multi_op():
            op = self.visit(ctx.multi_op())
            if op == '+': return AdditionExp([self.visit(e) for e in ctx.ground_f_exp()])
            elif op == '*': return MultiplicationExp([self.visit(e) for e in ctx.ground_f_exp()])
            else: raise AttributeError(ctx.multi_op())
        else: # should be '( - <expr> )'
            return OppositeExp(self.visit(ctx.ground_f_exp()))

    def visitConstraint_defs(self, ctx:antlrHDDLParser.Constraint_defsContext):
        return [self.visit(c) for c in ctx.constraint_def()]

    #############################################################################
    #############################################################################
    #############################################################################
    #############################################################################
    #############################################################################

    def visitProblem(self, ctx:antlrHDDLParser.ProblemContext):
        requirements = self.visit(ctx.require_def()) if ctx.require_def() else []
        objects = self.visit(ctx.p_object_declaration()) if ctx.p_object_declaration() else []
        init = self.visit(ctx.p_init())
        goal = self.visit(ctx.p_goal()) if ctx.p_goal() else EmptyGD()
        (htn_parameters, htn_network) = self.visit(ctx.p_htn()) if ctx.p_htn() else ([], None)
        # constraints
        metric = self.visit(ctx.metric_spec()) if ctx.metric_spec() else None
        return HDDLProblem(ctx.NAME(0),
                 ctx.NAME(1), # domain name
                 requirements=requirements,
                 objects=objects,
                 init=init,
                 goal=goal,
                 htn=htn_network,
                 htn_parameters=htn_parameters,
                 metric=metric)

    def visitP_htn(self, ctx:antlrHDDLParser.P_htnContext):
        params = self.visit(ctx.typed_var_list()) if ctx.typed_var_list() else []
        tn = self.visit(ctx.tasknetwork_def())
        return (params, tn)
                      

    ############################ NotSupported GD ################################################

    def visitGd_ltl_at_end(self, ctx:antlrHDDLParser.Gd_ltl_at_endContext):
        raise NotSupported(ctx)

    def visitGd_ltl_always(self, ctx:antlrHDDLParser.Gd_ltl_alwaysContext):
        raise NotSupported(ctx)

    def visitGd_ltl_sometime(self, ctx:antlrHDDLParser.Gd_ltl_sometimeContext):
        raise NotSupported(ctx)

    def visitGd_ltl_at_most_once(self, ctx:antlrHDDLParser.Gd_ltl_at_most_onceContext):
        raise NotSupported(ctx)

    def visitGd_ltl_sometime_after(self, ctx:antlrHDDLParser.Gd_ltl_sometime_afterContext):
        raise NotSupported(ctx)

    def visitGd_ltl_sometime_before(self, ctx:antlrHDDLParser.Gd_ltl_sometime_beforeContext):
        raise NotSupported(ctx)

    def visitGd_preference(self, ctx:antlrHDDLParser.Gd_preferenceContext):
        raise NotSupported(ctx)

    ############################ NotSupported HTN ################################################

    def visitConstraint_def(self, ctx:antlrHDDLParser.Constraint_defContext):
        raise NotSupported(ctx)

    def visitCausallink_defs(self, ctx:antlrHDDLParser.Causallink_defsContext):
        raise NotSupported(ctx)

    def visitCausallink_def(self, ctx:antlrHDDLParser.Causallink_defContext):
        raise NotSupported(ctx)

    def visitTyped_var(self, ctx:antlrHDDLParser.Typed_varContext):
        raise NotSupported(ctx)

    def visitP_constraint(self, ctx:antlrHDDLParser.P_constraintContext):
        raise NotSupported(ctx)