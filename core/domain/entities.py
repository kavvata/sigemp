from dataclasses import asdict, dataclass
from datetime import date
from typing import Any


@dataclass
class BaseEntity:
    def to_dict(self, exclude=None):
        entity_dict = asdict(self)

        if exclude:
            for field in exclude:
                try:
                    del entity_dict[field]
                except KeyError:
                    pass  # ignore fields that don't exist

        return entity_dict


@dataclass
class TimeStampableEntity(BaseEntity):
    criado_em: date = None
    criado_por: Any = None
    alterado_em: date = None
    alterado_por: Any = None
    removido_em: date = None

    def to_dict(self, exclude=None):
        entity_dict = super().to_dict(exclude)
        if exclude:
            if "timestamps" in exclude:
                try:
                    del entity_dict["criado_em"]
                    del entity_dict["criado_por"]
                    del entity_dict["alterado_em"]
                    del entity_dict["alterado_por"]
                    del entity_dict["removido_em"]
                except KeyError:
                    pass  # in case one of the fields were excluded individually

        return entity_dict
