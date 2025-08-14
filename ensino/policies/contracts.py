from abc import ABC, abstractmethod


class CampusPolicy(ABC):
    def __init__(self, user) -> None:
        super.__init__()
        self.user = user

    @abstractmethod
    def pode_listar(self) -> bool:
        pass

    @abstractmethod
    def pode_criar(self) -> bool:
        pass

    @abstractmethod
    def pode_editar(self, campus) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, campus) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, campus) -> bool:
        pass
