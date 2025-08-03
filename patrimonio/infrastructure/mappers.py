from django.forms import model_to_dict
from patrimonio.domain.entities import (
    BemEntity,
    EstadoConservacaoEntity,
    GrauFragilidadeEntity,
    TipoBemEntity,
    MarcaModeloEntity,
)
from patrimonio.models import (
    Bem,
    EstadoConservacao,
    GrauFragilidade,
    TipoBem,
    MarcaModelo,
)


class TipoBemMapper:
    @staticmethod
    def from_model(model: TipoBem):
        return TipoBemEntity(**model_to_dict(model))

    @staticmethod
    def from_dict(data: dict):
        return TipoBemEntity(**data)


class EstadoConservacaoMapper:
    @staticmethod
    def from_model(model: EstadoConservacao):
        return EstadoConservacaoEntity(**model_to_dict(model))

    @staticmethod
    def from_dict(data: dict):
        return EstadoConservacaoEntity(**data)


class GrauFragilidadeMapper:
    @staticmethod
    def from_model(model: GrauFragilidade):
        return GrauFragilidadeEntity(**model_to_dict(model))

    @staticmethod
    def from_dict(data: dict):
        return GrauFragilidadeEntity(**data)


class MarcaModeloMapper:
    @staticmethod
    def from_model(model: MarcaModelo):
        return MarcaModeloEntity(**model_to_dict(model))

    @staticmethod
    def from_dict(data: dict):
        return MarcaModeloEntity(**data)


class BemMapper:
    @staticmethod
    def from_model(model: Bem):
        return BemEntity(**model_to_dict(model))

    @staticmethod
    def from_dict(data: dict):
        return BemEntity(**data)
