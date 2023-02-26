from django.db import models
from django.db.models import Sum, F

from admin_personal_account.models import PersonalAccount
from admin_tariff.models import Tariff
from admin_service.models import Service


# Create your models here.
class Receipt(models.Model):
    def set_total_price(self):
        result = ReceiptService.objects.filter(receipt=self.pk).aggregate(
            total=Sum(F('consumption') * F('price_unit')))['total']
        self.total_price = result or 0

    @property
    def address_for_excel(self):
        apartment = self.personal_account.apartment
        owner = apartment.owner
        return f'{owner.last_name} {owner.first_name[0]}. {owner.middle_name[0]}. {apartment.house.address} ' \
               f'квартира {apartment.number}'

    class StatusName(models.TextChoices):
        PAID = 'Оплачена', 'Оплачена'
        PRE_PAID = 'Частично оплачена', 'Частично оплачена'
        NOT_PAID = 'Не оплачена', 'Не оплачена'

    personal_account = models.ForeignKey(PersonalAccount, on_delete=models.CASCADE, null=True)
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

    @property
    def price(self):
        return self.price_unit * self.consumption
