from django.utils import timezone

from typing import Any
from emprestimo.domain.entities import TipoOcorrenciaEntity
from emprestimo.infrastructure.mappers import TipoOcorrenciaMapper
from emprestimo.repositories.contracts import TipoOcorrenciaRepository
from emprestimo.models import TipoOcorrencia


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
        self, tipo_ocorrencia: TipoOcorrenciaEntity, user: Any
    ):
        return TipoOcorrenciaMapper.from_model(
            TipoOcorrencia.objects.create(
                **tipo_ocorrencia.to_dict(["timestamps", "id"]),
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
