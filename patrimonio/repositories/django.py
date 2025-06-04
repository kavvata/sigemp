from typing import override
from patrimonio.models import TipoBem
from patrimonio.repositories.contracts import TipoBemRepository


class DjTipoBemRepository(TipoBemRepository):
    @override
    def cadastrar_tipo_bem(self, descricao: str) -> any:
        return TipoBem.objects.create(descricao=descricao)

    @override
    def editar_tipo_bem(self, id: int, descricao: str) -> any:
        tipo_bem = None

        try:
            tipo_bem = TipoBem.objects.get(pk=id, ativo=True)
        except TipoBem.DoesNotExist:
            raise Exception(f"Tipo de bem com id {id} não encontrado.")

        try:
            TipoBem.objects.get(descricao=descricao, ativo=True)
            raise Exception(f"Descrição de tipo de bem '{descricao}' ja cadastrado.")
        except TipoBem.DoesNotExist:
            # ok
            pass

        tipo_bem.descricao = descricao
        tipo_bem.save()

        return tipo_bem

    @override
    def remover_tipo_bem(self, id: int, descricao: str) -> any:
        tipo_bem = None
        try:
            tipo_bem = TipoBem.objects.get(pk=id, ativo=True)
        except TipoBem.DoesNotExist:
            raise Exception(f"Tipo de bem com id {id} não encontrado.")

        tipo_bem.ativo = False
        tipo_bem.save()

        return tipo_bem
