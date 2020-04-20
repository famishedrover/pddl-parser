class UnknownLiteral(object):
    def __init__(self, formula):
        self.__formula = formula
    @property
    def formula(self):
        return self.__formula
    def __str__(self):
        return '(unknown ' + str(self.formula) + ')'

class OrBelief(object):
    def __init__(self, literals):
        self.__literals = literals
    @property
    def literals(self):
        return self.__literals
    def __str__(self):
        pddl = '(or'
        for a in self.literals:
            pddl += ' ' + str(a)
        pddl += ')'
        return pddl

class OneOfBelief(object):
    def __init__(self, literals):
        self.__literals = literals
    @property
    def literals(self):
        return self.__literals
    def __str__(self):
        pddl = '(oneof'
        for a in self.literals:
            pddl += ' ' + str(a)
        pddl += ')'
        return pddl
