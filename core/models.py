from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Timestampable(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True, null=True)
    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="criou_%(app_label)s_%(class)s",
    )

    alterado_em = models.DateTimeField(auto_now=True, null=True)
    alterado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="atualizou_%(app_label)s_%(class)s",
    )

    removido_em = models.DateTimeField(null=True)

    class Meta:
        abstract = True
