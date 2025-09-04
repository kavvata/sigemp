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


class Aluno(Timestampable, models.Model):
    nome = models.CharField(null=False, blank=False, max_length=255)
    nome_responsavel = models.CharField(null=True, blank=False, max_length=255)
    cpf = models.CharField(null=False, blank=False, max_length=11)
    email = models.CharField(null=False, blank=False, max_length=255)
    matricula = models.CharField(null=False, blank=False, max_length=65)
    telefone = models.CharField(null=False, blank=False, max_length=65)

    forma_selecao: models.ForeignKey(
        FormaSelecao,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    curso = models.ForeignKey(
        Curso,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.nome} ({self.matricula})"
