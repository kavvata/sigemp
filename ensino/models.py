from django.db import models

from core.models import Timestampable


# Create your models here.
class Campus(Timestampable, models.Model):
    sigla = models.CharField(null=False, blank=False, max_length=32)
    nome = models.CharField(null=False, blank=False, max_length=255)

    def __str__(self) -> str:
        return self.nome


class Curso(Timestampable, models.Model):
    sigla = models.CharField(null=False, blank=False, max_length=32)
    nome = models.CharField(null=False, blank=False, max_length=255)
    campus = models.ForeignKey(
        Campus, null=False, blank=False, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.nome} ({self.campus.sigla})"


class FormaSelecao(Timestampable, models.Model):
    descricao = models.CharField(null=False, blank=False, max_length=255)
    periodo_inicio = models.DateField(null=False, blank=False)
    periodo_fim = models.DateField(null=False, blank=False)

    def __str__(self) -> str:
        return self.descricao
