from abc import ABC, abstractmethod
from typing import Any

from emprestimo.domain.entities import TipoOcorrenciaEntity


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
