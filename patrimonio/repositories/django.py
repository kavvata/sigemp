from datetime import date
from typing import override

from django.contrib.auth.models import User
from patrimonio.models import TipoBem
from patrimonio.repositories.contracts import TipoBemRepository


class DjTipoBemRepository(TipoBemRepository):
    @override
    def listar_tipos_bem(self):
        return TipoBem.objects.filter(removido_em__isnull=True)

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
    def remover_tipo_bem(self, id: int, descricao: str, user: User) -> TipoBem:
        tipo_bem = None

        try:
            tipo_bem = TipoBem.objects.get(pk=id, removido_em__isnull=True)
        except TipoBem.DoesNotExist as e:
            e.add_note(f"Tipo de bem com id {id} não encontrado.")
            raise e

        tipo_bem.removido_em = date.today()
        tipo_bem.save()

        return tipo_bem
