from django.contrib.auth.models import User
from django.utils import timezone

from typing import Any, Optional
from emprestimo.domain.entities import TipoOcorrenciaEntity, EmprestimoEntity
from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.infrastructure.mappers import TipoOcorrenciaMapper, EmprestimoMapper
from emprestimo.repositories.contracts import (
    TipoOcorrenciaRepository,
    EmprestimoRepository,
)
from emprestimo.models import TipoOcorrencia, Emprestimo


class DjangoTipoOcorrenciaRepository(TipoOcorrenciaRepository):
    def listar_tipos_ocorrencia(self):
        return [
            TipoOcorrenciaMapper.from_model(tipo)
            for tipo in TipoOcorrencia.objects.filter(
                removido_em__isnull=True
            ).order_by("descricao")
        ]

    def buscar_por_id(self, id: int):
        try:
            tipo = TipoOcorrencia.objects.get(pk=id, removido_em__isnull=True)
        except TipoOcorrencia.DoesNotExist as e:
            e.add_note(f"Tipo de ocorrência com id '{id}' não encontrado.")
            raise e
        else:
            return TipoOcorrenciaMapper.from_model(tipo)

    def cadastrar_tipo_ocorrencia(
        self, tipo_ocorrencia: TipoOcorrenciaEntity, user: User
    ):
        return TipoOcorrenciaMapper.from_model(
            TipoOcorrencia.objects.create(
                **tipo_ocorrencia.to_dict(["timestamps", "id"]), criado_por=user
            )
        )

    def editar_tipo_ocorrencia(self, tipo_ocorrencia: TipoOcorrenciaEntity, user: Any):
        try:
            TipoOcorrencia.objects.filter(pk=tipo_ocorrencia.id).update(
                **tipo_ocorrencia.to_dict(["timestamps", "id"]), alterado_por=user
            )
        except TipoOcorrencia.DoesNotExist as e:
            e.add_note(
                f"Tipo de ocorrência com id '{tipo_ocorrencia.id}' não encontrado."
            )
            raise e

        return TipoOcorrenciaMapper.from_model(
            TipoOcorrencia.objects.get(pk=tipo_ocorrencia.id)
        )

    def remover_tipo_ocorrencia(self, id: int, user: Any):
        try:
            tipo_ocorrencia = TipoOcorrencia.objects.get(pk=id)
        except TipoOcorrencia.DoesNotExist as e:
            e.add_note(f"Tipo de ocorrência com id  '{id}' não encontrado.")
            raise e

        tipo_ocorrencia.removido_em = timezone.now()
        tipo_ocorrencia.alterado_por = user
        tipo_ocorrencia.save()
        return TipoOcorrenciaMapper.from_model(tipo_ocorrencia)


class DjangoEmprestimoRepository(EmprestimoRepository):
    def listar_emprestimos(self):
        return [
            EmprestimoMapper.from_model(emprestimo)
            for emprestimo in Emprestimo.objects.filter(
                removido_em__isnull=True
            ).order_by("-data_emprestimo")
        ]

    def buscar_por_id(self, id: int):
        try:
            emprestimo = Emprestimo.objects.get(pk=id, removido_em__isnull=True)
        except TipoOcorrencia.DoesNotExist as e:
            e.add_note(f"Emprestimo com id '{id}' não encontrado.")
            raise e
        else:
            return EmprestimoMapper.from_model(emprestimo)

    def buscar_ativo_por_bem(self, bem_id: int) -> Optional[EmprestimoEntity]:
        try:
            emprestimo = EmprestimoMapper.from_model(
                Emprestimo.objects.get(bem_id=bem_id, estado=EmprestimoEstadoEnum.ATIVO)
            )
        except Emprestimo.DoesNotExist:
            return None

        return emprestimo

    def buscar_ativos_por_aluno(
        self, aluno_id: int
    ) -> Optional[list[EmprestimoEntity]]:
        return [
            EmprestimoMapper.from_model(e)
            for e in Emprestimo.objects.filter(
                aluno_id=aluno_id, estado=EmprestimoEstadoEnum.ATIVO
            )
        ]

    def cadastrar_emprestimo(self, emprestimo: EmprestimoEntity, user: User):
        return EmprestimoMapper.from_model(
            Emprestimo.objects.create(
                **emprestimo.to_dict(
                    [
                        "bem_patrimonio",
                        "bem_descricao",
                        "aluno_nome",
                        "aluno_matricula",
                        "timestamps",
                        "id",
                    ]
                ),
                criado_por=user,
            )
        )

    def editar_emprestimo(self, emprestimo: EmprestimoEntity, user: Any):
        try:
            Emprestimo.objects.filter(pk=emprestimo.id).update(
                **emprestimo.to_dict(
                    [
                        "bem_patrimonio",
                        "bem_descricao",
                        "aluno_nome",
                        "aluno_matricula",
                        "timestamps",
                        "id",
                    ]
                ),
                alterado_por=user,
            )
        except Emprestimo.DoesNotExist as e:
            e.add_note(f"Emprestimo com id '{emprestimo.id}' não encontrado.")
            raise e

        return EmprestimoMapper.from_model(Emprestimo.objects.get(pk=emprestimo.id))

    def remover_emprestimo(self, id: int, user: Any):
        try:
            emprestimo = Emprestimo.objects.get(pk=id)
        except Emprestimo.DoesNotExist as e:
            e.add_note(f"Emprestimo com id '{id}' não encontrado.")
            raise e

        emprestimo.removido_em = timezone.now()
        emprestimo.alterado_por = user
        emprestimo.save()
        return EmprestimoMapper.from_model(emprestimo)
