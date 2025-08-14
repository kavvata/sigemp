from dataclasses import dataclass

from core.domain.entities import TimeStampableEntity


@dataclass(kw_only=True)
class CampusEntity(TimeStampableEntity):
    sigla: str
    nome: str
    id: int = None
