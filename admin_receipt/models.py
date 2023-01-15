from django.db import models
from admin_apartment.models import Apartment
from admin_tariff.models import Tariff
from admin_service.models import Service


# Create your models here.
class Receipt(models.Model):
    class StatusName(models.TextChoices):
        PAID = 'Оплачена', 'Оплачена'
        PRE_PAID = 'Частично оплачена', 'Частично оплачена'
        NOT_PAID = 'Не оплачена', 'Не оплачена'

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, null=True, on_delete=models.SET_NULL)
    is_complete = models.BooleanField(default=True)
    date = models.DateField()
    number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=StatusName.choices)
    period_start = models.DateField()
    period_end = models.DateField()
    services = models.ManyToManyField(Service, through='ReceiptService')


class ReceiptService(models.Model):
    receipt_id = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    consumption = models.FloatField()
    price_unit = models.FloatField()
