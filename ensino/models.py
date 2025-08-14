from django.db import models

from core.models import Timestampable


# Create your models here.
class Campus(Timestampable, models.Model):
    sigla = models.CharField(null=False, blank=False, max_length=32)
    descricao = models.CharField(null=False, blank=False, max_length=255)
