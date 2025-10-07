from dataclasses import dataclass
from typing import Optional

from core.domain.entities import TimeStampableEntity


@dataclass(kw_only=True)
class TipoBemEntity(TimeStampableEntity):
    descricao: str
    id: int = None


@dataclass(kw_only=True)
class EstadoConservacaoEntity(TimeStampableEntity):
    descricao: str
    nivel: int
    id: int = None


@dataclass(kw_only=True)
class GrauFragilidadeEntity(TimeStampableEntity):
    descricao: str
    nivel: int
    id: int = None


@dataclass(kw_only=True)
class MarcaModeloEntity(TimeStampableEntity):
    marca: str
    modelo: str
    id: int = None


@dataclass(kw_only=True)
class BemEntity(TimeStampableEntity):
    descricao: str
    patrimonio: str
    tipo_id: int
    grau_fragilidade_id: int
    estado_conservacao_id: int
    marca_modelo_id: int
    id: Optional[int] = None
    estado_conservacao_descricao: Optional[str] = None
    tipo_descricao: Optional[str] = None

    def to_dict(self, exclude: list[str] = None):
        if exclude is not None:
            exclude.append("estado_conservacao_descricao")
            exclude.append("tipo_descricao")
        else:
            exclude = ["estado_conservacao_descricao", "tipo_descricao"]

        return super().to_dict(exclude)
