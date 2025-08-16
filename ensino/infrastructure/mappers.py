from django.forms import model_to_dict
from ensino.domain.entities import CampusEntity
from ensino.models import Campus


class CampusMapper:
    @staticmethod
    def from_model(instance: Campus):
        return CampusEntity(**model_to_dict(instance))

    @staticmethod
    def from_dict(data: dict):
        return CampusEntity(**data)
