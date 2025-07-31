from django.forms import model_to_dict
from patrimonio.domain.entities import EstadoConservacaoEntity, TipoBemEntity
from patrimonio.models import EstadoConservacao, TipoBem


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
