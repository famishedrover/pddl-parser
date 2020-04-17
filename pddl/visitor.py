from antlr4 import *
from .parser.PDDLLexer import PDDLLexer
from .parser.PDDLParser import *
from .parser.PDDLVisitor import PDDLVisitor as AbstractPDDLVisitor

from .domain import Domain, Type, Constant, Variable, Predicate, Action
from .formula import AtomicFormula, NotFormula, AndFormula, WhenEffect

class PDDLVisitor(AbstractPDDLVisitor):

    def visitDomain(self, ctx):
        return Domain(ctx.name.text,
            self.visit(ctx.requirements) if ctx.requirements else None,
            self.visit(ctx.types) if ctx.types else None,
            self.visit(ctx.constants) if ctx.constants else None,
            self.visit(ctx.predicates) if ctx.predicates else None,
            [self.visit(o) for o in ctx.operators])

    def visitRequireDef(self, ctx):
        return [k.text for k in ctx.keys]

    def visitTypesDef(self, ctx):
        return self.visit(ctx.types)

    def visitTypedList(self, ctx):
        if ctx.supertype:
            typedList = [Type(t.text, ctx.supertype.text) for t in ctx.types]
        else:
            typedList = [Type(t.text) for t in ctx.types]
        if ctx.typedList():
            typedList += self.visit(ctx.typedList())
        return typedList

    def visitTypedObjList(self, ctx):
        if ctx.objtype:
            typedList = [Constant(t.text, ctx.objtype.text) for t in ctx.names]
        else:
            typedList = [Constant(t.text) for t in ctx.names]
        if ctx.typedObjList():
            typedList += self.visit(ctx.typedObjList())
        return typedList

    def visitTypedVarList(self, ctx):
        if ctx.vartype:
            typedList = [Variable(t.text, ctx.vartype.text) for t in ctx.names]
        else:
            typedList = [Variable(t.text) for t in ctx.names]
        if ctx.typedVarList():
            typedList += self.visit(ctx.typedVarList())
        return typedList

    def visitConstantsDef(self, ctx):
        return self.visit(ctx.typedObjList())

    def visitPredicatesDef(self, ctx):
        return [self.visit(p) for p in ctx.predicateDef()]

    def visitPredicateDef(self, ctx):
        return Predicate(str(ctx.predicate.NAME()), self.visit(ctx.typedVarList()))

    def visitStructureDef(self, ctx):
        if ctx.actionDef():
            return self.visit(ctx.actionDef())

    def visitActionDef(self, ctx):
        return Action(ctx.name.text,
            parameters=(self.visit(ctx.parameters) if ctx.parameters else None),
            precondition=(self.visit(ctx.precondition) if ctx.precondition else None),
            effect=(self.visit(ctx.effect) if ctx.effect else None),
            observe=(self.visit(ctx.observe) if ctx.observe else None))

    def visitGoalDef(self, ctx):
        if ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.atomicFormula():
            return self.visit(ctx.atomicFormula())
        elif ctx.AND():
            return AndFormula([self.visit(gd) for gd in ctx.ands])

    def visitLiteral(self, ctx):
        if ctx.NOT():
            return NotFormula(self.visit(ctx.atomicFormula()))
        else:
            return self.visit(ctx.atomicFormula())

    def visitAtomicFormula(self, ctx):
        return AtomicFormula(str(ctx.predicate.NAME()), [self.visit(t) for t in ctx.arguments])

    def visitTerm(self, ctx):
        if ctx.NAME():
            return ctx.name.text
        else:
            return ctx.variable.text

    def visitEffectDef(self, ctx):
        if ctx.AND():
            return AndFormula([self.visit(gd) for gd in ctx.ands])
        else:
            return self.visit(ctx.cEffect(0))

    def visitCEffect(self, ctx):
        if ctx.FORALL():
            return # TODO
        elif ctx.WHEN():
            return WhenEffect(self.visit(ctx.goalDef()), self.visit(ctx.condEffect()))
        else:
            return self.visit(ctx.literal())

    def visitCondEffect(self, ctx):
        if ctx.AND():
            return AndFormula([self.visit(gd) for gd in ctx.ands])
        else:
            return self.visit(ctx.literal(0))

    def visitObserveDef(self, ctx):
        return self.visit(ctx.atomicFormula())
