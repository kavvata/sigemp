from abc import ABC, abstractmethod


class TipoBemRepository(ABC):
    @abstractmethod
    def listar_tipos_bem(self) -> any:
        pass

    @abstractmethod
    def cadastrar_tipo_bem(self, descricao: str) -> any:
        pass

    @abstractmethod
    def editar_tipo_bem(self, id: int, descricao: str) -> any:
        pass

    @abstractmethod
    def remover_tipo_bem(self, id: int, descricao: str) -> any:
        pass
