import datetime

from django.db import models


# Create your models here.


class Software(models.Model):
    arch = models.CharField(max_length=255, null=True, blank=True)
    guid = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    version = models.CharField(max_length=50, null=True)
    install_date = models.DateField(default=datetime.date.today, null=True, blank=True)

    def __str__(self):
        return f"{self.name}: {self.version}"

class Computer(models.Model):
    device_uid = models.CharField(unique=True, max_length=255, null=True)
    softwares = models.ManyToManyField(Software)

    def __str__(self):
