from abc import ABC, abstractmethod
from typing import Any


class TipoBemRepository(ABC):
    @abstractmethod
    def listar_tipos_bem(self) -> Any:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Any:
        pass

    @abstractmethod
    def cadastrar_tipo_bem(self, descricao: str, user: Any) -> Any:
        pass

    @abstractmethod
    def editar_tipo_bem(self, id: int, descricao: str, user: Any) -> Any:
        pass

    @abstractmethod
    def remover_tipo_bem(self, id: int, user: Any) -> Any:
        pass
