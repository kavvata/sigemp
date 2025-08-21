from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from core.domain.entities import TimeStampableEntity


@dataclass(kw_only=True)
class CampusEntity(TimeStampableEntity):
    sigla: str
    nome: str
    id: int = None


@dataclass(kw_only=True)
class CursoEntity(TimeStampableEntity):
    sigla: str
    nome: str
    campus_id: int
    id: int = None
    campus_sigla: Optional[str] = None

    def __str__(self) -> str:
        return f"{self.nome} ({self.campus_sigla})"


@dataclass(kw_only=True)
class FormaSelecaoEntity(TimeStampableEntity):
    descricao: str
    periodo_inicio: datetime
    periodo_fim: datetime
    id: Optional[int] = None
