from abc import ABC, abstractmethod
from typing import Any


class TipoOcorrenciaPolicy(ABC):
    def __init__(self, user) -> None:
        super().__init__()
        self.user = user

    @abstractmethod
    def pode_listar(self) -> bool:
        pass

    @abstractmethod
    def pode_criar(self) -> bool:
        pass

    @abstractmethod
    def pode_editar(self, tipo_ocorrencia) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, tipo_ocorrencia) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, tipo_ocorrencia) -> bool:
        pass


class EmprestimoPolicy(ABC):
    def __init__(self, user) -> None:
        super().__init__()
        self.user = user

    @abstractmethod
    def pode_listar(self) -> bool:
        pass

    @abstractmethod
    def pode_criar(self) -> bool:
        pass

    @abstractmethod
    def pode_editar(self, emprestimo) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, emprestimo) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, emprestimo) -> bool:
        pass

    @abstractmethod
    def pode_gerar_termos(self, emprestimo) -> bool:
        pass


class OcorrenciaPolicy(ABC):
    def __init__(self, user) -> None:
        super().__init__()
        self.user = user

    @abstractmethod
    def pode_listar(self) -> bool:
        pass

    @abstractmethod
    def pode_criar(self) -> bool:
        pass

    @abstractmethod
    def pode_editar(self, ocorrencia) -> bool:
        pass

    @abstractmethod
    def pode_remover(self, ocorrencia) -> bool:
        pass

    @abstractmethod
    def pode_visualizar(self, ocorrencia) -> bool:
        pass
