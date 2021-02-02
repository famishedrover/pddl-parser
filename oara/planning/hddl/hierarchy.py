from typing import List, Union, Tuple, Dict, Optional
from itertools import count

from .types import TypedVariable, TypedObject
from .action import Action
from .formula import AtomicFormula
from .gd import GD, EmptyGD
from .effect import EFFECT, EmptyEffect


class Task(Action):
    """HDDL task."""

    def __str__(self) -> str:
        return f"""
    (:task {self.name}
        :parameters ({' '.join(map(str, self.parameters))})
        :precondition {self.precondition}
        :effect {self.effect}
    )"""

    def ground(self, assignment: Dict[str, str]) -> 'Task':
        params = []
        for p in self.parameters:
            if p.name in assignment:
                params.append(TypedObject(assignment[p.name], p.types))
            else:
                params.append(p)
        return Task(self.name,
            parameters=params,
            precondition=self.precondition.ground(assignment)
            )


class Method:
    """HDDL method.

    method_def : '(' ':method' method_symbol
      ':parameters' '(' typed_var_list ')'
      ':task' '(' task_symbol var_or_const* ')'
      (':precondition' gd)?
      (':effect' effect)?
      tasknetwork_def;

    :param name: method name
    :param task: task implemented by the method
    :param parameters: method parameters
    :param precondition: method precondition
    :param tn: method task network
    """

    def __init__(self, 
                 name: str, 
                 task: AtomicFormula,
                 parameters: List[TypedVariable] = [],
                 precondition: GD = EmptyGD(),
                 effect: EFFECT = EmptyEffect(),
                 tn: 'TaskNetwork' = None):
        self.__name = name
        self.__task = task
        self.__parameters = parameters
        self.__precondition = precondition
        self.__effect = effect
        self.__network = tn

    def __str__(self) -> str:
        return f"""
    (:method {self.__name}
        :parameters ({' '.join(map(str, self.__parameters))})
        :task {self.__task}
        :precondition {self.__precondition}
        :effect {self.__effect}
        {self.__network}
    )"""

    def __eq__(self, other) -> bool:
        return self.__name == other.__name

    def __hash__(self):
        return self.__name.__hash__()


class Subtask(AtomicFormula):
    """ Subtask definition

    subtask_def : ('(' task_symbol var_or_const* ')' | '(' subtask_id '(' task_symbol var_or_const* ')' ')');
    subtask_id : NAME;

    :param subtask_id: id used in network orders
    :param task: task predicate
    :param arguments: task arguments
    """

    _ids = count(0)

    def __init__(self, subtask_id: Optional[str], task: str, arguments: List[str]):
        super().__init__(task, arguments)
        self.__id = f"global_subtask_{next(self._ids)}" if subtask_id is None else subtask_id

    @property
    def id(self) -> str:
        return self.__id

    def __str__(self):
        return f"({self.__id} {super().__str__()})"

    def __eq__(self, other) -> bool:
        return self.__id == other.__id

    def __hash__(self):
        return self.__id.__hash__()


class Ordering(AtomicFormula):
    """ Ordering relation between two subtasks.

    ordering_def : '(' '<' subtask_id subtask_id ')' | '(' subtask_id '<' subtask_id ')';

    :param before: id of the task before
    :param after: id of the task after
    """
    def __init__(self, before: str, after: str):
        super().__init__('<', [before, after])


class TaskNetwork:
    """Task network model.

    tasknetwork_def :
      ((':subtasks' | ':tasks' | ':ordered-subtasks' | ':ordered-tasks') subtask_defs)?
      ((':ordering' | ':order') ordering_defs)?
      (':constraints' constraint_defs)?
      ((':causal-links' | ':causallinks') causallink_defs)?
      ')';

    :param subtasks: subtasks of the method
    :param ordering: ordering relation between subtasks
    :param constraints:
    :param causal_links:
    """

    def __init__(self,
                 subtasks: List[Subtask] = [],
                 ordering: List[Ordering] = []):
        self.__subtasks = subtasks
        self.__ordering = ordering

    def __str__(self) -> str:
        nl = '\n\t\t'
        if len(self.__subtasks) <= 1:
            return f":subtasks {self.__subtasks[0] if self.__subtasks else '()'}"
        elif len(self.__ordering) <= 1:
            return f""":subtasks (and 
                {nl.join(map(str, self.__subtasks))}
            )
            :ordering {self.__ordering[0] if self.__ordering else '()'}"""
        else:
            return f""":subtasks (and 
        {nl.join(map(str, self.__subtasks))}
    )
    :ordering (and 
        {nl.join(map(str, self.__ordering))}
    )"""


class OrderedTaskNetwork(TaskNetwork):
    """ Ordered Task network model.

    tasknetwork_def :
      ((':subtasks' | ':tasks' | ':ordered-subtasks' | ':ordered-tasks') subtask_defs)?
      ((':ordering' | ':order') ordering_defs)?
      (':constraints' constraint_defs)?
      ((':causal-links' | ':causallinks') causallink_defs)?
      ')';

    :param subtasks: subtasks of the method
    :param constraints:
    :param causal_links:
    """

    def __init__(self,
                 subtasks: List[Subtask] = []):

        if len(subtasks) < 2:
            ordering = []
        else:
            ordering = [Ordering(first.id, second.id) for (first, second) in zip(subtasks, subtasks[1:])]
        super().__init__(subtasks, ordering)
