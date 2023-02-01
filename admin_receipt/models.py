from django.db import models
from django.db.models import Sum, F

from admin_apartment.models import Apartment
from admin_tariff.models import Tariff
from admin_service.models import Service


# Create your models here.
class Receipt(models.Model):
    def set_total_price(self):
        result = ReceiptService.objects.filter(receipt=self.pk).aggregate(
            total=Sum(F('consumption') * F('price_unit')))['total']
        self.total_price = result or 0

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
    total_price = models.FloatField(default=0)

    class Meta:
        ordering = ['-pk']


class ReceiptService(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    consumption = models.FloatField()
    price_unit = models.FloatField()
