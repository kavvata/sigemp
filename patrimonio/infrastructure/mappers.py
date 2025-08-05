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
        model_dict = model_to_dict(
            model,
        )

        # FIXME: hacky solution, please refactor me later.

        model_dict["tipo_id"] = model_dict["tipo"]
        del model_dict["tipo"]

        model_dict["estado_conservacao_id"] = model_dict["estado_conservacao"]
        del model_dict["estado_conservacao"]

        model_dict["grau_fragilidade_id"] = model_dict["grau_fragilidade"]
        del model_dict["grau_fragilidade"]

        model_dict["marca_modelo_id"] = model_dict["marca_modelo"]
        del model_dict["marca_modelo"]

        entity = BemMapper.from_dict(model_dict)

        return entity

    @staticmethod
    def from_dict(data: dict):
        return BemEntity(**data)
