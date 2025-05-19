from abc import ABC, abstractmethod


class Result(ABC):
    def __init__(self, mensagem="") -> None:
        self.mensagem = mensagem

    @abstractmethod
    def __bool__(self):
        pass


class ResultSuccess(Result):
    def __init__(self, value: any, mensagem="") -> None:
        self.value = value
        super().__init__(mensagem)

    def __bool__(self):
        return True


class ResultError(Result):
    def __init__(self, mensagem="") -> None:
        super().__init__(mensagem)

    def __bool__(self):
        return False
