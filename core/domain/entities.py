from dataclasses import asdict, dataclass
from datetime import date
from typing import Any


@dataclass
class BaseEntity:
    def to_dict(self):
        return asdict(self)


@dataclass
class TimeStampableEntity(BaseEntity):
    criado_em: date = None
    criado_por: Any = None
    alterado_em: date = None
    alterado_por: Any = None
    removido_em: date = None
