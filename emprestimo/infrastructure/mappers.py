from django.forms import model_to_dict
from emprestimo.domain.entities import EmprestimoEntity, TipoOcorrenciaEntity
from emprestimo.models import Emprestimo, TipoOcorrencia


class TipoOcorrenciaMapper:
    @staticmethod
    def from_model(instance: TipoOcorrencia):
        return TipoOcorrenciaEntity(**model_to_dict(instance))

    @staticmethod
    def from_dict(data: dict):
        return TipoOcorrenciaEntity(**data)


class EmprestimoMapper:
    @staticmethod
    def from_dict(data: dict):
        return EmprestimoEntity(**data)

    @staticmethod
    def from_model(model: Emprestimo):
        model_dict = model_to_dict(model)

        model_dict["devolucao_ciente_por_id"] = model_dict["devolucao_ciente_por"].id
        del model_dict["devolucao_ciente_por"]

        model_dict["bem_id"] = model_dict["bem"].id
        del model_dict["bem"]

        model_dict["aluno_id"] = model_dict["aluno"].id
        del model_dict["aluno"]

        return EmprestimoMapper.from_dict(model_dict)
