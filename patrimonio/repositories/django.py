from django.utils import timezone
from typing import override

from django.contrib.auth.models import User
from patrimonio.models import EstadoConservacao, TipoBem
from patrimonio.repositories.contracts import (
    EstadoConservacaoRepository,
    TipoBemRepository,
)


class DjTipoBemRepository(TipoBemRepository):
    @override
    def listar_tipos_bem(self):
        return TipoBem.objects.filter(removido_em__isnull=True).order_by("descricao")

    @override
    def buscar_por_id(self, id: int):
        tipo_bem = None

        try:
            tipo_bem = TipoBem.objects.get(pk=id, removido_em__isnull=True)
        except TipoBem.DoesNotExist as e:
            e.add_note(f"Tipo de bem com id {id} não encontrado.")
            raise e
        else:
            return tipo_bem

    @override
    def cadastrar_tipo_bem(self, descricao: str, user: User) -> TipoBem:
        return TipoBem.objects.create(descricao=descricao, criado_por=user)

    @override
    def editar_tipo_bem(self, id: int, descricao: str, user: User) -> TipoBem:
        try:
            tipo_bem = TipoBem.objects.get(pk=id, removido_em__isnull=True)
        except TipoBem.DoesNotExist as e:
            e.add_note(f"Tipo de bem com id {id} não encontrado.")
            raise e

        tipo_bem.descricao = descricao
        tipo_bem.alterado_por = user
        tipo_bem.save()

        return tipo_bem

    @override
    def remover_tipo_bem(self, id: int, user: User) -> TipoBem:
        try:
            tipo_bem = TipoBem.objects.get(pk=id, removido_em__isnull=True)
        except TipoBem.DoesNotExist as e:
            e.add_note(f"Tipo de bem com id {id} não encontrado.")
            raise e

        tipo_bem.removido_em = timezone.now()
        tipo_bem.alterado_por = user
        tipo_bem.save()

        return tipo_bem


class DjangoEstadoConservacaoRepository(EstadoConservacaoRepository):
    @override
    def listar_estados_conservacao(self):
        return EstadoConservacao.objects.filter(removido_em__isnull=True).order_by(
            "nivel"
        )

    @override
    def buscar_por_id(self, id: int):
        try:
            estado_conservacao = EstadoConservacao.objects.get(
                pk=id, removido_em__isnull=True
            )
        except EstadoConservacao.DoesNotExist as e:
            e.add_note(f"Estado de conservacao com id {id} não encontrado.")
            raise e
        else:
            return estado_conservacao

    @override
    def cadastrar_estado_conservacao(self, descricao: str, nivel: int, user: User):
        return EstadoConservacao.objects.create(
            descricao=descricao, nivel=nivel, criado_por=user
        )

    def editar_estado_conservacao(
        self, id: int, descricao: str, nivel: int, user: User
    ):
        try:
            estado = EstadoConservacao.objects.get(pk=id)
        except EstadoConservacao.DoesNotExist as e:
            e.add_note(f"Estado de conservacao com id {id} não encontrado.")

        estado.alterado_por = user
        estado.descricao = descricao
        estado.nivel = nivel
        estado.save()
        return estado

    def remover_estado_conservacao(self, id: int, user: User):
        try:
            estado = EstadoConservacao.objects.get(pk=id)
        except EstadoConservacao.DoesNotExist as e:
            e.add_note(f"Estado de conservacao com id {id} não encontrado.")

        estado.removido_em = timezone.now()
        estado.alterado_por = user
        estado.save()
