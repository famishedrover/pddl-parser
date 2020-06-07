class Task(object):
    def __init__(self, name, parameters=[]):
        self.__name = name
        self.__parameters = parameters
    @property
    def name(self):
        return self.__name
    @property
    def parameters(self):
        return self.__parameters

class Method(object):
    def __init__(self, name, task, parameters=None, precondition=None, tn=None):
        self.__name = name
        self.__task = task
        self.__parameters = parameters
        self.__precondition = precondition
        self.__tn = tn
    @property
    def name(self):
        return self.__name
    @property
    def task(self):
        return self.__task
    @property
    def parameters(self):
        return self.__parameters
    @property
    def precondition(self):
        return self.__precondition
    @property
    def network(self):
        return self.__tn

class TaskNetwork(object):
    def __init__(self, subtasks, ordering):
        self.__subtasks = subtasks
        self.__ordering = ordering
    @property
    def subtasks(self):
        return self.__subtasks
    @property
    def ordering(self):
        return self.__ordering
