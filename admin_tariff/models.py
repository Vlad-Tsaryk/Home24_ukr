from django.db import models
from admin_service.models import Service


# Create your models here.
class Tariff(models.Model):
    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': "Тариф із таким ім'ям вже існує!"
    })
    description = models.TextField()
    services = models.ManyToManyField(Service, through='TariffService')
    date_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_edit']


class TariffService(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.FloatField()
