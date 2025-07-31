from typing import override

from django.contrib.auth.models import User
from django.utils import timezone

from patrimonio.infrastructure.mappers import EstadoConservacaoMapper, TipoBemMapper
from patrimonio.models import EstadoConservacao, GrauFragilidade, TipoBem, MarcaModelo
from patrimonio.repositories.contracts import (
    EstadoConservacaoRepository,
    GrauFragilidadeRepository,
    MarcaModeloRepository,
    TipoBemRepository,
)


class DjangoTipoBemRepository(TipoBemRepository):
    @override
    def listar_tipos_bem(self):
        return [
            TipoBemMapper.from_model(tipo_bem)
            for tipo_bem in TipoBem.objects.filter(removido_em__isnull=True).order_by(
                "descricao"
            )
        ]

    @override
    def buscar_por_id(self, id: int):
        tipo_bem = None

        try:
            tipo_bem = TipoBem.objects.get(pk=id, removido_em__isnull=True)
        except TipoBem.DoesNotExist as e:
            e.add_note(f"Tipo de bem com id {id} não encontrado.")
            raise e
        else:
            return TipoBemMapper.from_model(tipo_bem)

    @override
    def cadastrar_tipo_bem(self, descricao: str, user: User) -> TipoBem:
        return TipoBemMapper.from_model(
            TipoBem.objects.create(descricao=descricao, criado_por=user)
        )

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

        return TipoBemMapper.from_model(tipo_bem)

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

        return TipoBemMapper.from_model(tipo_bem)


class DjangoEstadoConservacaoRepository(EstadoConservacaoRepository):
    @override
    def listar_estados_conservacao(self):
        return [
            EstadoConservacaoMapper.from_model(estado_conservacao)
            for estado_conservacao in EstadoConservacao.objects.filter(
                removido_em__isnull=True
            ).order_by("nivel")
        ]

    @override
    def buscar_por_id(self, id: int):
        try:
            estado = EstadoConservacao.objects.get(pk=id, removido_em__isnull=True)
        except EstadoConservacao.DoesNotExist as e:
            e.add_note(f"Estado de conservacao com id {id} não encontrado.")
            raise e
        else:
            return EstadoConservacaoMapper.from_model(estado)

    @override
    def cadastrar_estado_conservacao(self, descricao: str, nivel: int, user: User):
        return EstadoConservacaoMapper.from_model(
            EstadoConservacao.objects.create(
                descricao=descricao, nivel=nivel, criado_por=user
            )
        )

    def editar_estado_conservacao(
        self, id: int, descricao: str, nivel: int, user: User
    ):
        try:
            estado = EstadoConservacao.objects.get(pk=id)
        except EstadoConservacao.DoesNotExist as e:
            e.add_note(f"Estado de conservacao com id {id} não encontrado.")
            raise e

        estado.alterado_por = user
        estado.descricao = descricao
        estado.nivel = nivel
        estado.save()
        return EstadoConservacaoMapper.from_model(estado)

    def remover_estado_conservacao(self, id: int, user: User):
        try:
            estado = EstadoConservacao.objects.get(pk=id)
        except EstadoConservacao.DoesNotExist as e:
            e.add_note(f"Estado de conservacao com id {id} não encontrado.")
            raise e

        estado.removido_em = timezone.now()
        estado.alterado_por = user
        estado.save()
        return EstadoConservacaoMapper.from_model(estado)


class DjangoGrauFragilidadeRepository(GrauFragilidadeRepository):
    @override
    def listar_grau_fragilidade(self):
        return GrauFragilidade.objects.filter(removido_em__isnull=True).order_by(
            "nivel"
        )

    @override
    def buscar_por_id(self, id: int):
        try:
            grau_fragilidade = GrauFragilidade.objects.get(
                pk=id, removido_em__isnull=True
            )
        except GrauFragilidade.DoesNotExist as e:
            e.add_note(f"Grau de fragilidade com id {id} não encontrado.")
            raise e
        else:
            return grau_fragilidade

    @override
    def cadastrar_grau_fragilidade(self, descricao: str, nivel: int, user: User):
        return GrauFragilidade.objects.create(
            descricao=descricao, nivel=nivel, criado_por=user
        )

    def editar_grau_fragilidade(self, id: int, descricao: str, nivel: int, user: User):
        try:
            grau = GrauFragilidade.objects.get(pk=id)
        except GrauFragilidade.DoesNotExist as e:
            e.add_note(f"Grau de fragilidade com id {id} não encontrado.")
            raise e

        grau.alterado_por = user
        grau.descricao = descricao
        grau.nivel = nivel
        grau.save()
        return grau

    def remover_grau_fragilidade(self, id: int, user: User):
        try:
            grau = GrauFragilidade.objects.get(pk=id)
        except GrauFragilidade.DoesNotExist as e:
            e.add_note(f"Grau de fragilidade com id {id} não encontrado.")
            raise e

        grau.removido_em = timezone.now()
        grau.alterado_por = user
        grau.save()


class DjangoMarcaModeloRepository(MarcaModeloRepository):
    @override
    def listar_marca_modelo(self):
        return MarcaModelo.objects.filter(removido_em__isnull=True).order_by(
            "marca", "modelo"
        )

    @override
    def buscar_por_id(self, id: int):
        try:
            marca_modelo = MarcaModelo.objects.get(pk=id, removido_em__isnull=True)
        except MarcaModelo.DoesNotExist as e:
            e.add_note(f"MarcaModelo com id {id} não encontrado.")
            raise e
        else:
            return marca_modelo

    @override
    def cadastrar_marca_modelo(self, marca: str, modelo: str, user: User):
        return MarcaModelo.objects.create(marca=marca, modelo=modelo, criado_por=user)

    def editar_marca_modelo(self, id: int, marca: str, modelo: str, user: User):
        try:
            marca_modelo = MarcaModelo.objects.get(pk=id)
        except MarcaModelo.DoesNotExist as e:
            e.add_note(f"MarcaModelo com id {id} não encontrado.")
            raise e

        marca_modelo.alterado_por = user
        marca_modelo.marca = marca
        marca_modelo.modelo = modelo
        marca_modelo.save()
        return marca_modelo

    def remover_marca_modelo(self, id: int, user: User):
        try:
            marca_modelo = MarcaModelo.objects.get(pk=id)
        except MarcaModelo.DoesNotExist as e:
            e.add_note(f"MarcaModelo com id {id} não encontrado.")
            raise e

        marca_modelo.removido_em = timezone.now()
        marca_modelo.alterado_por = user
        marca_modelo.save()
