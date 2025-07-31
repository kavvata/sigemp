from patrimonio.domain.entities import TipoBemEntity
from patrimonio.models import TipoBem


class TipoBemMapper:
    @staticmethod
    def from_model(model: TipoBem):
        return TipoBemEntity(id=model.id, descricao=model.descricao)

    @staticmethod
    def from_dict(data: dict):
        return TipoBemEntity(**data)
