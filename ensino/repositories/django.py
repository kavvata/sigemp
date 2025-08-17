from django.contrib.auth.models import User
from django.utils import timezone
from ensino.infrastructure.mappers import CampusMapper, CursoMapper
from ensino.models import Campus, Curso
from ensino.repositories.contracts import CampusRepository, CursoRepository
from ensino.domain.entities import CampusEntity, CursoEntity


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


class DjangoCursoRepository(CursoRepository):
    def listar_cursos(self):
        return [
            CursoMapper.from_model(curso)
            for curso in Curso.objects.filter(removido_em__isnull=True).order_by("nome")
        ]

    def buscar_por_id(self, id: int):
        try:
            curso = Curso.objects.get(pk=id, removido_em__isnull=True)
        except Curso.DoesNotExist as e:
            e.add_note(f"Curso com id '{id}' não encontrado.")
            raise e
        else:
            return CursoMapper.from_model(curso)

    def cadastrar_curso(self, curso: CursoEntity, user: User):
        return CursoMapper.from_model(
            Curso.objects.create(
                **curso.to_dict(["timestamps", "id"]),
                alterado_por=user,
            )
        )

    def editar_curso(self, curso: CursoEntity, user: User):
        try:
            Curso.objects.filter(pk=curso.id).update(
                **curso.to_dict(["timestamps", "id"]), alterado_por=user
            )
        except Curso.DoesNotExist as e:
            e.add_note(f"Curso com id '{curso.id}' não encontrado.")
            raise e

        return CursoMapper.from_model(Curso.objects.get(pk=curso.id))

    def remover_curso(self, id: int, user: User):
        try:
            curso = Curso.objects.get(pk=id)
        except Curso.DoesNotExist as e:
            e.add_note(f"Curso com id '{id}' não encontrado.")
            raise e

        curso.removido_em = timezone.now()
        curso.alterado_por = user
        curso.save()
        return CursoMapper.from_model(curso)
