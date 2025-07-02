from django.db import models

from core.models import Timestampable


# Create your models here.
class TipoBem(Timestampable, models.Model):
    descricao = models.CharField(null=False, blank=False, max_length=255)

    def __str__(self) -> str:
        return self.descricao


class EstadoConservacao(Timestampable, models.Model):
    descricao = models.CharField(null=False, blank=False, max_length=255)

    def __str__(self) -> str:
        return self.descricao
