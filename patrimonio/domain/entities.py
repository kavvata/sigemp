from dataclasses import dataclass

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
    id: int = None
