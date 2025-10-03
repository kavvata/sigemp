from dataclasses import dataclass
from datetime import date
from typing import Optional

from core.domain.entities import TimeStampableEntity
from emprestimo.domain.types import EmprestimoEstadoEnum


@dataclass(kw_only=True)
class TipoOcorrenciaEntity(TimeStampableEntity):
    descricao: str
    id: int = None


@dataclass(kw_only=True)
class EmprestimoEntity(TimeStampableEntity):
    data_emprestimo: date
    data_devolucao_prevista: date
    aluno_id: int
    bem_id: int
    data_devolucao: Optional[date] = None
    devolucao_ciente_por_id: Optional[int] = None
    bem_descricao: Optional[str] = None
    bem_patrimonio: Optional[str] = None
    aluno_nome: Optional[str] = None
    aluno_matricula: Optional[str] = None
    estado: EmprestimoEstadoEnum
    id: Optional[int] = None
    observacoes: str = ""

    def to_dict(
        self,
        exclude=[
            "bem_patrimonio",
            "bem_descricao",
            "aluno_nome",
            "aluno_matricula",
            "timestamps",
        ],
    ):
        return super().to_dict(exclude)


@dataclass(kw_only=True)
class OcorrenciaEntity(TimeStampableEntity):
    data_ocorrencia: date
    emprestimo_id: int
    tipo_id: int
    tipo_descricao: Optional[str] = None
    bem_descricao: Optional[str] = None
    bem_patrimonio: Optional[str] = None
    id: Optional[int] = None
    cancelado_em: Optional[date] = None
    cancelado_por_id: Optional[int] = None
    motivo_cancelamento: Optional[str] = None
    aluno_nome: Optional[str] = None
    aluno_matricula: Optional[str] = None
    descricao: Optional[str] = None
