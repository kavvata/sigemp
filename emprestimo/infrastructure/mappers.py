from django.forms import model_to_dict
from emprestimo.domain.entities import (
    EmprestimoEntity,
    OcorrenciaEntity,
    TipoOcorrenciaEntity,
)
from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.models import Emprestimo, Ocorrencia, TipoOcorrencia


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

        if "devolucao_ciente_por" in model_dict.keys():
            if model_dict["devolucao_ciente_por"] is not None:
                model_dict["devolucao_ciente_por_id"] = model_dict.pop(
                    "devolucao_ciente_por"
                )
            else:
                del model_dict["devolucao_ciente_por"]

        model_dict["bem_id"] = model_dict.pop("bem")
        model_dict["bem_descricao"] = model.bem.descricao
        model_dict["bem_patrimonio"] = model.bem.patrimonio

        model_dict["aluno_id"] = model_dict.pop("aluno")
        model_dict["aluno_nome"] = model.aluno.nome
        model_dict["aluno_matricula"] = model.aluno.matricula

        # NOTE: hacky solution
        estado_value = model_dict.get("estado")
        if estado_value is not None:
            model_dict["estado"] = EmprestimoEstadoEnum(estado_value)

        return EmprestimoEntity(**model_dict)


class OcorrenciaMapper:
    @staticmethod
    def from_dict(data: dict):
        return OcorrenciaEntity(**data)

    @staticmethod
    def from_model(model: Ocorrencia):
        model_dict = model_to_dict(model)

        if "cancelado_por" in model_dict.keys():
            if model_dict["cancelado_por"] is not None:
                model_dict["cancelado_por_id"] = model_dict.pop("cancelado_por")
            else:
                del model_dict["cancelado_por"]

        model_dict["emprestimo_id"] = model_dict.pop("emprestimo")
        model_dict["tipo_id"] = model_dict.pop("tipo")
        model_dict["tipo_descricao"] = model.tipo.descricao
        model_dict["bem_descricao"] = model.emprestimo.bem.descricao
        model_dict["bem_patrimonio"] = model.emprestimo.bem.patrimonio
        model_dict["aluno_nome"] = model.emprestimo.aluno.nome
        model_dict["aluno_matricula"] = model.emprestimo.aluno.matricula

        return OcorrenciaEntity(**model_dict)
