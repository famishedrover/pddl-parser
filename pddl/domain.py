class Type(object):
    def __init__(self, name, type=None):
        self.__name = name
        self.__type = type
    @property
    def name(self):
        return self.__name
    @property
    def type(self):
        return self.__type
    def __str__(self):
        if self.type:
            return "{} - {}".format(self.name, self.type)
        else:
            return self.name

class Constant(Type):
    pass

class Variable(Type):
    pass

class Predicate(object):
    def __init__(self, name, variables=[]):
        self.__name = name
        self.__variables = variables
    @property
    def name(self):
        return self.__name
    @property
    def variables(self):
        return self.__variables

class Action(object):
    def __init__(self, name, parameters=[], precondition=None, effect=None, observe=None):
        self.__name = name
        self.__parameters = parameters
        self.__precondition = precondition
        self.__effect = effect
        self.__observe = observe
    @property
    def name(self):
        return self.__name
    @property
    def parameters(self):
        return self.__parameters
    @property
    def precondition(self):
        return self.__precondition
    @property
    def effect(self):
        return self.__effect
    @property
    def observe(self):
        return self.__observe

class Domain(object):
    def __init__(self, name, requirements=[], types=[], constants=[],
            predicates=[], actions=[], tasks=[], methods=[]):
        self.__name = name
        self.__requirements = requirements
        self.__types = types
        self.__constants = constants
        self.__predicates = predicates
        self.__actions = actions
        self.__tasks = tasks
        self.__methods = methods

    @property
    def name(self):
        return self.__name
    @property
    def requirements(self):
        return self.__requirements
    @property
    def types(self):
        return self.__types
    @property
    def constants(self):
        return self.__constants
    @property
    def predicates(self):
        return self.__predicates
    @property
    def actions(self):
        return self.__actions
    @property
    def tasks(self):
        return self.__tasks
    @property
    def methods(self):
        return self.__methods
