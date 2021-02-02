from typing import List, Union


class Metric:
    """ Problem metric.

    metric_spec : '(' ':metric' optimization ground_f_exp')';
    optimization : 'minimize' | 'maximize';

    """
    def __init__(self, optimization: str, expression: str):
        self.__optimization = optimization
        self.__expression = expression

    def __str__(self) -> str:
        return f"(:metric {self.__optimization} {self.__expression})"