from django.db import models


# Create your models here.
class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Service(models.Model):
    name = models.CharField(max_length=50, unique=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True)
    is_counter = models.BooleanField(default=False)
