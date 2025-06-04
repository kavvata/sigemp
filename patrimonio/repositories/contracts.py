from abc import ABC, abstractmethod


class TipoBemRepository(ABC):
    @abstractmethod
    def listar_tipos_bem(self):
        pass

    @abstractmethod
    def buscar_tipo_bem_por_id(self, id: int):
        pass

    @abstractmethod
    def cadastrar_tipo_bem(self, descricao: str):
        pass

    @abstractmethod
    def editar_tipo_bem(self, id: int, descricao: str):
        pass

    @abstractmethod
    def remover_tipo_bem(self, id: int):
        pass
