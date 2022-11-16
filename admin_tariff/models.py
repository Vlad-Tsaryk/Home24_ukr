from django.db import models
from admin_service.models import Service


# Create your models here.
class Tariff(models.Model):
    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': "Тариф с таким именем уже существует!"
    })
    description = models.TextField()
    services = models.ManyToManyField(Service, through='TariffService', null=True)
    date_edit = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_edit']


class TariffService(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.FloatField()
