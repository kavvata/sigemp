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


class EstadoConservacaoRepository(ABC):
    @abstractmethod
    def listar_estados_conservacao(self) -> Any:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Any:
        pass

    @abstractmethod
    def cadastrar_estado_conservacao(
        self, descricao: str, nivel: int, user: Any
    ) -> Any:
        pass

    @abstractmethod
    def editar_estado_conservacao(
        self, id: int, descricao: str, nivel: int, user: Any
    ) -> Any:
        pass

    @abstractmethod
    def remover_estado_conservacao(self, id: int, user: Any) -> Any:
        pass


class GrauFragilidadeRepository(ABC):
    @abstractmethod
    def listar_grau_fragilidade(self) -> Any:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Any:
        pass

    @abstractmethod
    def cadastrar_grau_fragilidade(self, descricao: str, nivel: int, user: Any) -> Any:
        pass

    @abstractmethod
    def editar_grau_fragilidade(
        self, id: int, descricao: str, nivel: int, user: Any
    ) -> Any:
        pass

    @abstractmethod
    def remover_grau_fragilidade(self, id: int, user: Any) -> Any:
        pass
