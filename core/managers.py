from django.db import models


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(removido_em__isnull=True)

    def with_deleted(self):
        return super().get_queryset()

    def only_deleted(self):
        return super().get_queryset().filter(removido_em__isnull=False)

    def restore(self, *args, **kwargs):
        qs = self.only_deleted().filter(*args, **kwargs)
        qs.update(removido_em=None)
        return qs


class DeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(removido_em__isnull=False)

    def restore(self, *args, **kwargs):
        qs = self.filter(*args, **kwargs)
        qs.update(removido_em=None)
        return qs
