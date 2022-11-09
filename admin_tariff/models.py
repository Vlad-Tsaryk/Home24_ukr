from django.db import models
from admin_service.models import Service


# Create your models here.
class Tariff(models.Model):
    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': "Тариф с таким именем уже существует!"
    })
    description = models.TextField()
    services = models.ManyToManyField(Service, through='TariffService')


class TariffService(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    price = models.FloatField()
