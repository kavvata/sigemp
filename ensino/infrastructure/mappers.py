from django.forms import model_to_dict
from ensino.domain.entities import CampusEntity, CursoEntity
from ensino.models import Campus, Curso


class CampusMapper:
    @staticmethod
    def from_model(instance: Campus):
        return CampusEntity(**model_to_dict(instance))

    @staticmethod
    def from_dict(data: dict):
        return CampusEntity(**data)


class CursoMapper:
    @staticmethod
    def from_model(instance: Curso):
        model_dict = model_to_dict(instance)
        model_dict["campus_id"] = model_dict.pop("campus")
        model_dict["campus_sigla"] = instance.campus.sigla
        return CursoEntity(**model_dict)

    @staticmethod
    def from_dict(data: dict):
        return CursoEntity(**data)
