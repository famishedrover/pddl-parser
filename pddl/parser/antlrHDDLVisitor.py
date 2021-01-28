# Generated from antlrHDDL.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .antlrHDDLParser import antlrHDDLParser
else:
    from antlrHDDLParser import antlrHDDLParser

# This class defines a complete generic visitor for a parse tree produced by antlrHDDLParser.

class antlrHDDLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by antlrHDDLParser#hddl_file.
    def visitHddl_file(self, ctx:antlrHDDLParser.Hddl_fileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#domain.
    def visitDomain(self, ctx:antlrHDDLParser.DomainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#domain_symbol.
    def visitDomain_symbol(self, ctx:antlrHDDLParser.Domain_symbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#require_def.
    def visitRequire_def(self, ctx:antlrHDDLParser.Require_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#require_defs.
    def visitRequire_defs(self, ctx:antlrHDDLParser.Require_defsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#type_def.
    def visitType_def(self, ctx:antlrHDDLParser.Type_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#type_def_list.
    def visitType_def_list(self, ctx:antlrHDDLParser.Type_def_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#new_types.
    def visitNew_types(self, ctx:antlrHDDLParser.New_typesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#const_def.
    def visitConst_def(self, ctx:antlrHDDLParser.Const_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#predicates_def.
    def visitPredicates_def(self, ctx:antlrHDDLParser.Predicates_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#atomic_formula_skeleton.
    def visitAtomic_formula_skeleton(self, ctx:antlrHDDLParser.Atomic_formula_skeletonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#funtions_def.
    def visitFuntions_def(self, ctx:antlrHDDLParser.Funtions_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#comp_task_def.
    def visitComp_task_def(self, ctx:antlrHDDLParser.Comp_task_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#task_def.
    def visitTask_def(self, ctx:antlrHDDLParser.Task_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#task_symbol.
    def visitTask_symbol(self, ctx:antlrHDDLParser.Task_symbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#method_def.
    def visitMethod_def(self, ctx:antlrHDDLParser.Method_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#tasknetwork_def.
    def visitTasknetwork_def(self, ctx:antlrHDDLParser.Tasknetwork_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#method_symbol.
    def visitMethod_symbol(self, ctx:antlrHDDLParser.Method_symbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#subtask_defs.
    def visitSubtask_defs(self, ctx:antlrHDDLParser.Subtask_defsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#subtask_def.
    def visitSubtask_def(self, ctx:antlrHDDLParser.Subtask_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#subtask_id.
    def visitSubtask_id(self, ctx:antlrHDDLParser.Subtask_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#ordering_defs.
    def visitOrdering_defs(self, ctx:antlrHDDLParser.Ordering_defsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#ordering_def.
    def visitOrdering_def(self, ctx:antlrHDDLParser.Ordering_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#constraint_defs.
    def visitConstraint_defs(self, ctx:antlrHDDLParser.Constraint_defsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#constraint_def.
    def visitConstraint_def(self, ctx:antlrHDDLParser.Constraint_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#causallink_defs.
    def visitCausallink_defs(self, ctx:antlrHDDLParser.Causallink_defsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#causallink_def.
    def visitCausallink_def(self, ctx:antlrHDDLParser.Causallink_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#action_def.
    def visitAction_def(self, ctx:antlrHDDLParser.Action_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd.
    def visitGd(self, ctx:antlrHDDLParser.GdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_empty.
    def visitGd_empty(self, ctx:antlrHDDLParser.Gd_emptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_conjuction.
    def visitGd_conjuction(self, ctx:antlrHDDLParser.Gd_conjuctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_disjuction.
    def visitGd_disjuction(self, ctx:antlrHDDLParser.Gd_disjuctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_negation.
    def visitGd_negation(self, ctx:antlrHDDLParser.Gd_negationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_implication.
    def visitGd_implication(self, ctx:antlrHDDLParser.Gd_implicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_existential.
    def visitGd_existential(self, ctx:antlrHDDLParser.Gd_existentialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_universal.
    def visitGd_universal(self, ctx:antlrHDDLParser.Gd_universalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_equality_constraint.
    def visitGd_equality_constraint(self, ctx:antlrHDDLParser.Gd_equality_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_ltl_at_end.
    def visitGd_ltl_at_end(self, ctx:antlrHDDLParser.Gd_ltl_at_endContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_ltl_always.
    def visitGd_ltl_always(self, ctx:antlrHDDLParser.Gd_ltl_alwaysContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_ltl_sometime.
    def visitGd_ltl_sometime(self, ctx:antlrHDDLParser.Gd_ltl_sometimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_ltl_at_most_once.
    def visitGd_ltl_at_most_once(self, ctx:antlrHDDLParser.Gd_ltl_at_most_onceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_ltl_sometime_after.
    def visitGd_ltl_sometime_after(self, ctx:antlrHDDLParser.Gd_ltl_sometime_afterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_ltl_sometime_before.
    def visitGd_ltl_sometime_before(self, ctx:antlrHDDLParser.Gd_ltl_sometime_beforeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#gd_preference.
    def visitGd_preference(self, ctx:antlrHDDLParser.Gd_preferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#effect.
    def visitEffect(self, ctx:antlrHDDLParser.EffectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#eff_empty.
    def visitEff_empty(self, ctx:antlrHDDLParser.Eff_emptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#eff_conjunction.
    def visitEff_conjunction(self, ctx:antlrHDDLParser.Eff_conjunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#eff_universal.
    def visitEff_universal(self, ctx:antlrHDDLParser.Eff_universalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#eff_conditional.
    def visitEff_conditional(self, ctx:antlrHDDLParser.Eff_conditionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#literal.
    def visitLiteral(self, ctx:antlrHDDLParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#neg_atomic_formula.
    def visitNeg_atomic_formula(self, ctx:antlrHDDLParser.Neg_atomic_formulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#p_effect.
    def visitP_effect(self, ctx:antlrHDDLParser.P_effectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#assign_op.
    def visitAssign_op(self, ctx:antlrHDDLParser.Assign_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#f_head.
    def visitF_head(self, ctx:antlrHDDLParser.F_headContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#f_exp.
    def visitF_exp(self, ctx:antlrHDDLParser.F_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#bin_op.
    def visitBin_op(self, ctx:antlrHDDLParser.Bin_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#multi_op.
    def visitMulti_op(self, ctx:antlrHDDLParser.Multi_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#atomic_formula.
    def visitAtomic_formula(self, ctx:antlrHDDLParser.Atomic_formulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#predicate.
    def visitPredicate(self, ctx:antlrHDDLParser.PredicateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#equallity.
    def visitEquallity(self, ctx:antlrHDDLParser.EquallityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#typed_var_list.
    def visitTyped_var_list(self, ctx:antlrHDDLParser.Typed_var_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#typed_obj_list.
    def visitTyped_obj_list(self, ctx:antlrHDDLParser.Typed_obj_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#typed_vars.
    def visitTyped_vars(self, ctx:antlrHDDLParser.Typed_varsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#typed_var.
    def visitTyped_var(self, ctx:antlrHDDLParser.Typed_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#typed_objs.
    def visitTyped_objs(self, ctx:antlrHDDLParser.Typed_objsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#new_consts.
    def visitNew_consts(self, ctx:antlrHDDLParser.New_constsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#var_type.
    def visitVar_type(self, ctx:antlrHDDLParser.Var_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#var_or_const.
    def visitVar_or_const(self, ctx:antlrHDDLParser.Var_or_constContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#term.
    def visitTerm(self, ctx:antlrHDDLParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#functionterm.
    def visitFunctionterm(self, ctx:antlrHDDLParser.FunctiontermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#func_symbol.
    def visitFunc_symbol(self, ctx:antlrHDDLParser.Func_symbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#problem.
    def visitProblem(self, ctx:antlrHDDLParser.ProblemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#p_object_declaration.
    def visitP_object_declaration(self, ctx:antlrHDDLParser.P_object_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#p_init.
    def visitP_init(self, ctx:antlrHDDLParser.P_initContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#init_el.
    def visitInit_el(self, ctx:antlrHDDLParser.Init_elContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#num_init.
    def visitNum_init(self, ctx:antlrHDDLParser.Num_initContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#p_goal.
    def visitP_goal(self, ctx:antlrHDDLParser.P_goalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#p_htn.
    def visitP_htn(self, ctx:antlrHDDLParser.P_htnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#metric_spec.
    def visitMetric_spec(self, ctx:antlrHDDLParser.Metric_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#optimization.
    def visitOptimization(self, ctx:antlrHDDLParser.OptimizationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#ground_f_exp.
    def visitGround_f_exp(self, ctx:antlrHDDLParser.Ground_f_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by antlrHDDLParser#p_constraint.
    def visitP_constraint(self, ctx:antlrHDDLParser.P_constraintContext):
        return self.visitChildren(ctx)



del antlrHDDLParser