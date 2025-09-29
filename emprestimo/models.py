from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from core.models import Timestampable
from emprestimo.domain.types import EmprestimoEstadoEnum
from ensino.models import Aluno
from patrimonio.models import Bem


# Create your models here.
class TipoOcorrencia(Timestampable, models.Model):
    descricao = models.CharField(null=False, blank=False, max_length=255)

    def __str__(self) -> str:
        return f"{self.descricao}"


class Emprestimo(Timestampable, models.Model):
    data_emprestimo = models.DateField()
    data_devolucao_prevista = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)
    devolucao_ciente_por = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    bem = models.ForeignKey(
        Bem,
        on_delete=models.CASCADE,
    )
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
    )
    estado = models.IntegerField(
        choices=EmprestimoEstadoEnum.choices(),
    )
    observacoes = models.TextField(null=True, blank=True)
