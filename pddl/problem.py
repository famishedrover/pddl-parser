class Problem(object):
    def __init__(self, name, domain, init, goal=None, htn=None, requirements=[], objects=[]):
        self.__name = name
        self.__domain = domain
        self.__init = init
        self.__goal = goal
        self.__htn = htn
        self.__requirements = requirements
        self.__objects = objects
    @property
    def name(self):
        return self.__name
    @property
    def domain(self):
        return self.__domain
    @property
    def init(self):
        return self.__init
    @property
    def goal(self):
        return self.__goal
    @property
    def requirements(self):
        return self.__requirements
    @property
    def objects(self):
        return self.__objects
    @property
    def htn(self):
        return self.__htn
