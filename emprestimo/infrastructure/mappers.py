from django.forms import model_to_dict
from emprestimo.domain.entities import TipoOcorrenciaEntity
from emprestimo.models import TipoOcorrencia


class TipoOcorrenciaMapper:
    @staticmethod
    def from_model(instance: TipoOcorrencia):
        return TipoOcorrenciaEntity(**model_to_dict(instance))

    @staticmethod
    def from_dict(data: dict):
        return TipoOcorrenciaEntity(**data)
