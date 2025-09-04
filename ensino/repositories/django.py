from typing import Optional, Unpack
from django.contrib.auth.models import User
from django.utils import timezone
from ensino.infrastructure.mappers import (
    AlunoMapper,
    CampusMapper,
    CursoMapper,
    FormaSelecaoMapper,
)
from ensino.models import Aluno, Campus, Curso, FormaSelecao
from ensino.repositories.contracts import (
    AlunoRepository,
    CampusRepository,
    CursoRepository,
    FormaSelecaoRepository,
)
from ensino.domain.entities import (
    AlunoEntity,
    CampusEntity,
    CursoEntity,
    FormaSelecaoEntity,
)
from ensino.repositories.filters import AlunoFiltro


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
                **curso.to_dict(["timestamps", "id", "campus_sigla"]),
                alterado_por=user,
            )
        )

    def editar_curso(self, curso: CursoEntity, user: User):
        try:
            Curso.objects.filter(pk=curso.id).update(
                **curso.to_dict(["timestamps", "id", "campus_sigla"]), alterado_por=user
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


class DjangoFormaSelecaoRepository(FormaSelecaoRepository):
    def listar_formas_selecao(self):
        return [
            FormaSelecaoMapper.from_model(forma_selecao)
            for forma_selecao in FormaSelecao.objects.filter(
                removido_em__isnull=True
            ).order_by("periodo_inicio")
        ]

    def buscar_por_id(self, id: int):
        try:
            forma_selecao = FormaSelecao.objects.get(pk=id, removido_em__isnull=True)
        except FormaSelecao.DoesNotExist as e:
            e.add_note(f"FormaSelecao com id '{id}' não encontrado.")
            raise e
        else:
            return FormaSelecaoMapper.from_model(forma_selecao)

    def cadastrar_forma_selecao(self, forma_selecao: FormaSelecaoEntity, user: User):
        return FormaSelecaoMapper.from_model(
            FormaSelecao.objects.create(
                **forma_selecao.to_dict(["timestamps", "id", "campus_sigla"]),
                alterado_por=user,
            )
        )

    def editar_forma_selecao(self, forma_selecao: FormaSelecaoEntity, user: User):
        try:
            FormaSelecao.objects.filter(pk=forma_selecao.id).update(
                **forma_selecao.to_dict(["timestamps", "id", "campus_sigla"]),
                alterado_por=user,
            )
        except FormaSelecao.DoesNotExist as e:
            e.add_note(f"FormaSelecao com id '{forma_selecao.id}' não encontrado.")
            raise e

        return FormaSelecaoMapper.from_model(
            FormaSelecao.objects.get(pk=forma_selecao.id)
        )

    def remover_forma_selecao(self, id: int, user: User):
        try:
            forma_selecao = FormaSelecao.objects.get(pk=id)
        except FormaSelecao.DoesNotExist as e:
            e.add_note(f"FormaSelecao com id '{id}' não encontrado.")
            raise e

        forma_selecao.removido_em = timezone.now()
        forma_selecao.alterado_por = user
        forma_selecao.save()
        return FormaSelecaoMapper.from_model(forma_selecao)


class DjangoAlunoRepository(AlunoRepository):
    def listar_alunos(self):
        lista_alunos = Aluno.objects.filter(removido_em__isnull=True).order_by(
            "curso__nome", "nome"
        )

        return [AlunoMapper.from_model(aluno) for aluno in lista_alunos]

    def buscar_por_id(self, id: int):
        try:
            aluno = Aluno.objects.get(id=id)
        except Aluno.DoesNotExist as e:
            e.add_nome(f"Aluno com o id '{id} não encontrado.'")
            raise e

        return AlunoMapper.from_model(aluno)

    def buscar(self, **filtros: Unpack[AlunoFiltro]) -> Optional[AlunoEntity]:
        try:
            aluno = Aluno.objects.get(**filtros, removido_em__isnull=True)
        except Aluno.DoesNotExist as e:
            e.add_note(
                f"Não foi possível encontrar um aluno com o seguinte filtro: {filtros}"
            )
            raise e
        except Aluno.MultipleObjectsReturned as e:
            e.add_note(
                f"Mais de um aluno encontrado com o filtro especificado: \nfiltro: {filtros}"
            )

        return AlunoMapper.from_model(aluno)

    def cadastrar_aluno(self, aluno: AlunoEntity, user: User):
        return AlunoMapper.from_model(
            Aluno.objects.create(**aluno.to_dict(["timestamps", "id"])),
            criado_por=user,
        )

    def editar_aluno(self, aluno: AlunoEntity, user: User):
        try:
            Aluno.objects.filter(pk=aluno.id).update(
                **aluno.to_dict(["timestamps", "id"], alterado_por=user)
            )
        except Aluno.DoesNotExist as e:
            e.add_note(f"Aluno com id '{aluno.id}' não encontrado.")
            raise e

        return AlunoMapper.from_model(Aluno.objects.get(pk=aluno.id))

    def remover_aluno(self, id: int, user: User):
        try:
            aluno = Aluno.objects.get(pk=id)
        except Aluno.DoesNotExist as e:
            e.add_nome(f"Aluno com o id '{id} não encontrado.'")
            raise e
        aluno.removido_em = timezone.now()
        aluno.alterado_por = user

        return AlunoMapper.from_model(aluno)
