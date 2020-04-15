class AtomicFormula(object):
    def __init__(self, predicate, arguments=[]):
        self.__predicate = predicate
        self.__arguments = arguments
    @property
    def name(self):
        return self.__predicate
    @property
    def arguments(self):
        return self.__arguments
    def __str__(self):
        pddl = '(' + self.name
        for a in self.arguments:
            pddl += ' ' + str(a)
        pddl += ')'
        return pddl

class NotFormula(object):
    def __init__(self, formula):
        self.__formula = formula
    @property
    def formula(self):
        return self.__formula
    def __str__(self):
        return  '(not ' + str(self.formula) + ')'

class AndFormula(object):
    def __init__(self, formulas):
        self.__formulas = formulas
    @property
    def formulas(self):
        return self.__formulas
    def __str__(self):
        pddl = '(and'
        for a in self.formulas:
            pddl += ' ' + str(a)
        pddl += ')'
        return pddl

class WhenEffect(object):
    def __init__(self, condition, effect):
        self.__condition = condition
        self.__effect = effect
    @property
    def condition(self):
        return self.__condition
    @property
    def effect(self):
        return self.__effect
    def __str__(self):
        return '(when ' + str(self.condition) + ' ' + str(self.effect) + ')'
