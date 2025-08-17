from django.contrib.auth.models import User
from django.utils import timezone
from ensino.infrastructure.mappers import CampusMapper
from ensino.models import Campus
from ensino.repositories.contracts import CampusRepository
from ensino.domain.entities import CampusEntity


class DjangoCampusRepository(CampusRepository):
    def listar_campi(self):
        return [
            CampusMapper.from_model(campus)
            for campus in Campus.objects.filter(removido_em__isnull=True).order_by(
                "nome"
            )
        ]

    def buscar_por_id(self, id: int):
        try:
            campus = Campus.objects.get(pk=id, removido_em__isnull=True)
        except Campus.DoesNotExist as e:
            e.add_note(f"Campus com id '{id}' não encontrado.")
            raise e
        else:
            return CampusMapper.from_model(campus)

    def cadastrar_campus(self, campus: CampusEntity, user: User):
        return CampusMapper.from_model(
            Campus.objects.create(
                **campus.to_dict(["timestamps", "id"]),
                alterado_por=user,
            )
        )

    def editar_campus(self, campus: CampusEntity, user: User):
        try:
            Campus.objects.filter(pk=campus.id).update(
                **campus.to_dict(["timestamps", "id"]), alterado_por=user
            )
        except Campus.DoesNotExist as e:
            e.add_note(f"Campus com id '{campus.id}' não encontrado.")
            raise e

        return CampusMapper.from_model(Campus.objects.get(pk=campus.id))

    def remover_campus(self, id: int, user: User):
        try:
            campus = Campus.objects.get(pk=id)
        except Campus.DoesNotExist as e:
            e.add_note(f"Campus com id  '{id}' não encontrado.")
            raise e

        campus.removido_em = timezone.now()
        campus.alterado_por = user
        campus.save()
        return CampusMapper.from_model(campus)
