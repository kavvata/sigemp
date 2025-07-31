from dataclasses import dataclass


@dataclass
class TipoBemEntity:
    descricao: str
    id: int = None


@dataclass
class EstadoConservacaoEntity:
    descricao: str
    nivel: int
    id: int = None


@dataclass
class GrauFragilidadeEntity:
    descricao: str
    nivel: int
    id: int = None


@dataclass
class MarcaModeloEntity:
    marca: str
    modelo: str
    id: int = None


@dataclass
class BemEntity:
    descricao: str
    patrimonio: str
    tipo_id: TipoBemEntity
    grau_fragilidade_id: int
    estado_conservacao_id: int
    marca_modelo_id: int
    id: int = None
