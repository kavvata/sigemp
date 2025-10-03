from django.contrib.auth.models import User
from django.utils import timezone

from typing import Any, Optional
from emprestimo.domain.entities import (
    OcorrenciaEntity,
    TipoOcorrenciaEntity,
    EmprestimoEntity,
)
from emprestimo.domain.types import EmprestimoEstadoEnum
from emprestimo.infrastructure.mappers import (
    OcorrenciaMapper,
    TipoOcorrenciaMapper,
    EmprestimoMapper,
)
from emprestimo.repositories.contracts import (
    OcorrenciaRepository,
    TipoOcorrenciaRepository,
    EmprestimoRepository,
)
from emprestimo.models import Ocorrencia, TipoOcorrencia, Emprestimo


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
            for emprestimo in Emprestimo.objects.order_by("-data_emprestimo")
        ]

    def buscar_por_id(self, id: int):
        try:
            emprestimo = Emprestimo.objects.get(pk=id, removido_em__isnull=True)
        except Emprestimo.DoesNotExist as e:
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

        emprestimo.soft_delete()
        emprestimo.alterado_por = user
        emprestimo.save()
        return EmprestimoMapper.from_model(emprestimo)

    def registrar_devolucao(self, emprestimo: EmprestimoEntity, user: Any):
        try:
            model = Emprestimo.objects.get(pk=emprestimo.id)
        except Emprestimo.DoesNotExist as e:
            e.add_note(f"Emprestimo com id '{id}' não encontrado.")
            raise e

        model.data_devolucao = timezone.now()
        model.estado = EmprestimoEstadoEnum.FINALIZADO
        model.alterado_por = user
        model.devolucao_ciente_por = user
        model.save()

        return EmprestimoMapper.from_model(model)


class DjangoOcorrenciaRepository(OcorrenciaRepository):
    def listar_ocorrencias(self):
        return [
            OcorrenciaMapper.from_model(o)
            for o in Ocorrencia.objects.all().order_by("-data_ocorrencia")
        ]

    def listar_ocorrencias_do_aluno(self, aluno_id: int):
        return [
            OcorrenciaMapper.from_model(o).filter(emprestimo__aluno__id=aluno_id)
            for o in Ocorrencia.objects.all().order_by("-data_ocorrencia")
        ]

    def listar_ocorrencias_do_emprestimo(self, emprestimo_id: int):
        return [
            OcorrenciaMapper.from_model(o).filter(emprestimo_id=emprestimo_id)
            for o in Ocorrencia.objects.all().order_by("-data_ocorrencia")
        ]

    def listar_ocorrencias_do_bem(self, bem_id: int):
        return [
            OcorrenciaMapper.from_model(o).filter(emprestimo__bem_id=bem_id)
            for o in Ocorrencia.objects.all().order_by("-data_ocorrencia")
        ]

    def buscar_por_id(self, id: int):
        try:
            ocorrencia = Ocorrencia.objects.get(pk=id)
        except Ocorrencia.DoesNotExist:
            return None
        else:
            return EmprestimoMapper.from_model(ocorrencia)

    def cadastrar_ocorrencia(self, ocorrencia: OcorrenciaEntity, user: User):
        return OcorrenciaMapper.from_model(
            Ocorrencia.objects.create(
                **ocorrencia.to_dict(
                    [
                        "tipo_descricao",
                        "bem_descricao",
                        "bem_patrimonio",
                        "aluno_nome",
                        "aluno_matricula",
                        "timestamps",
                        "id",
                    ]
                ),
                criado_por=user,
            )
        )

    def editar_ocorrencia(self, ocorrencia: OcorrenciaEntity, user: User):
        return OcorrenciaMapper.from_model(
            Ocorrencia.objects.find(pk=ocorrencia.id).update(
                **ocorrencia.to_dict(
                    [
                        "tipo_descricao",
                        "bem_descricao",
                        "bem_patrimonio",
                        "aluno_nome",
                        "aluno_matricula",
                        "timestamps",
                    ]
                ),
                atualizado_por=user,
            )
        )

    def remover_ocorrencia(self, id: int, user: Any):
        try:
            ocorrencia = Ocorrencia.objects.get(pk=id)
        except Ocorrencia.DoesNotExist:
            return None

        return OcorrenciaMapper.from_model(ocorrencia.soft_delete())
