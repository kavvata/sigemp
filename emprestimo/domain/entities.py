from dataclasses import dataclass
from datetime import date
from typing import Optional

from core.domain.entities import TimeStampableEntity


@dataclass(kw_only=True)
class TipoOcorrenciaEntity(TimeStampableEntity):
    descricao: str
    id: int = None


@dataclass(kw_only=True)
class EmprestimoEntity(TimeStampableEntity):
    data_emprestimo: date
    data_devolucao_prevista: date
    data_devolucao: Optional[date]
    devolucao_ciente_por_id: Optional[int] = None
    bem_id: Optional[int] = None
    aluno_id: Optional[int] = None
    estado: int
    id: Optional[int] = None
