from dataclasses import dataclass

from core.domain.entities import TimeStampableEntity


@dataclass(kw_only=True)
class TipoOcorrenciaEntity(TimeStampableEntity):
    descricao: str
    id: int = None
