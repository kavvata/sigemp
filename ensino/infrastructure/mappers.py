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
        return CursoEntity(**model_to_dict(instance))

    @staticmethod
    def from_dict(data: dict):
        return CursoEntity(**data)
