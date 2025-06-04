from abc import ABC, abstractmethod


class TipoBemPolicy(ABC):
    @abstractmethod
    def pode_listar(self) -> bool:
        pass

    @abstractmethod
    def pode_criar(self) -> bool:
        pass

    @abstractmethod
    def pode_editar(self, tipo_bem) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, tipo_bem) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, tipo_bem) -> bool:
        pass
