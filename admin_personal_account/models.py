from django.db import models

from admin_apartment.models import Apartment
from admin_receipt.models import Receipt


# Create your models here.
class PersonalAccount(models.Model):
    @property
    def balance(self):
        result = self.transaction_set.all().filter(is_complete=True).aggregate(models.Sum('sum'))['sum__sum']
        for i in self.apartment.receipt_set.all().filter(is_complete=True).exclude(status=Receipt.StatusName.PAID):
            result -= i.total_price
        if result:
            return result
        else:
            return 0

    @staticmethod
    def total_debt():
        result = 0
        for personal_account in PersonalAccount.objects.all():
            balance = personal_account.balance
            if balance < 0:
                result += balance
        return '%.2f' % result

    @staticmethod
    def total_balance():
        result = 0
        for personal_account in PersonalAccount.objects.all():
            balance = personal_account.balance
            if balance > 0:
                result += balance
        return '%.2f' % result

    class StatusName(models.TextChoices):
        ACTIVE = 'Активен', 'Активен'
        DISABLED = 'Неактивен', 'Неактивен'

    status = models.CharField(choices=StatusName.choices, max_length=9)
    apartment = models.OneToOneField(Apartment, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.number
