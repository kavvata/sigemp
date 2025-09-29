from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from core.managers import DeletedManager, SoftDeleteManager


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

    objects = SoftDeleteManager()
    deleted_objects = DeletedManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.removido_em = timezone.now()
        self.save()
        self.refresh_from_db()

        return self

    def restore(self):
        self.removido_em = None
        self.save()
        self.refresh_from_db()
        return self

    def hard_delete(self):
        super().delete()

    @property
    def is_deleted(self):
        return self.removido_em is not None

    class Meta:
        abstract = True
