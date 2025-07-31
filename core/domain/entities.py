from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class TimeStampableEntity:
    criado_em: date = None
    criado_por: Any = None
    alterado_em: date = None
    alterado_por: Any = None
    removido_em: date = None
