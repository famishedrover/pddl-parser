class NotSupported(Exception):
    def __init__(self, feature):
        self.__feature = feature

    def __str__(self) -> str:
        return f"{self.__feature}: not supported"


class AlreadyDefined(Exception):
    def __init__(self, feature):
        self.__feature = feature

    def __str__(self) -> str:
        return f"{self.__feature}: already defined"
