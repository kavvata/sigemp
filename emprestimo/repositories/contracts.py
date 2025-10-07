from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Optional, Sequence, Unpack

from emprestimo.domain.entities import (
    OcorrenciaEntity,
    TipoOcorrenciaEntity,
    EmprestimoEntity,
)
from emprestimo.domain.types import EmprestimoFiltro, OcorrenciaFiltro


class TipoOcorrenciaRepository(ABC):
    @abstractmethod
    def listar_tipos_ocorrencia(self):
        pass

    @abstractmethod
    def buscar_por_id(self, id: int):
        pass

    @abstractmethod
    def cadastrar_tipo_ocorrencia(
        self, tipo_ocorrencia: TipoOcorrenciaEntity, user: Any
    ):
        pass

    @abstractmethod
    def editar_tipo_ocorrencia(self, tipo_ocorrencia: TipoOcorrenciaEntity, user: Any):
        pass

    @abstractmethod
    def remover_tipo_ocorrencia(self, id: int, user: Any):
        pass


class EmprestimoRepository(ABC):
    @abstractmethod
    def listar(self, **filtros: Unpack[EmprestimoFiltro]) -> list[EmprestimoEntity]:
        pass

    @abstractmethod
    def listar_emprestimos(self):
        pass

    @abstractmethod
    def listar_emprestimos_devolucao_proxima(
        self, data_devolucao: date
    ) -> Sequence[EmprestimoEntity]:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int):
        pass

    @abstractmethod
    def buscar_ativo_por_bem(self, bem_id: int) -> Optional[EmprestimoEntity]:
        pass

    @abstractmethod
    def buscar_ativos_por_aluno(
        self, aluno_id: int
    ) -> Optional[list[EmprestimoEntity]]:
        pass

    @abstractmethod
    def cadastrar_emprestimo(
        self, emprestimo: EmprestimoEntity, user: Any
    ) -> Optional[EmprestimoEntity]:
        pass

    @abstractmethod
    def editar_emprestimo(
        self, emprestimo: EmprestimoEntity, user: Any
    ) -> Optional[EmprestimoEntity]:
        pass

    @abstractmethod
    def remover_emprestimo(self, id: int, user: Any) -> Optional[EmprestimoEntity]:
        pass

    @abstractmethod
    def registrar_devolucao(self, emprestimo: EmprestimoEntity, user: Any):
        pass


class OcorrenciaRepository(ABC):
    @abstractmethod
    def listar(self, **filtros: Unpack[OcorrenciaFiltro]) -> list[OcorrenciaEntity]:
        pass

    @abstractmethod
    def listar_ocorrencias(self):
        pass

    @abstractmethod
    def listar_ocorrencias_do_aluno(self, aluno_id: int):
        pass

    @abstractmethod
    def listar_ocorrencias_do_bem(self, bem_id: int):
        pass

    @abstractmethod
    def listar_ocorrencias_do_emprestimo(self, emprestimo_id: int):
        pass

    @abstractmethod
    def buscar_por_id(self, id: int):
        pass

    @abstractmethod
    def cadastrar_ocorrencia(self, ocorrencia: OcorrenciaEntity, user: Any):
        pass

    @abstractmethod
    def editar_ocorrencia(self, ocorrencia: OcorrenciaEntity, user: Any):
        pass

    @abstractmethod
    def remover_ocorrencia(self, id: int, user: Any):
        pass
