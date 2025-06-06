from django.db import models


# Create your models here.
class TipoBem(models.Model):
    descricao = models.CharField(null=False, blank=False, max_length=255)
    ativo = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.descricao
