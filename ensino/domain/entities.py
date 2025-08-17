from dataclasses import dataclass

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
