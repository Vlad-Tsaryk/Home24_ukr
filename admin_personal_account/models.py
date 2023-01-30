from django.db import models

from admin_apartment.models import Apartment
from admin_receipt.models import Receipt


# Create your models here.
class PersonalAccount(models.Model):
    @property
    def balance(self):
        transaction_sum = self.transaction_set.all().filter(is_complete=True).aggregate(models.Sum('sum'))['sum__sum']
        receipt_sum = 0
        if not transaction_sum:
            transaction_sum = 0
        for i in self.apartment.receipt_set.all().filter(is_complete=True).exclude(status=Receipt.StatusName.PAID):
            receipt_sum += i.total_price
        return transaction_sum - receipt_sum

    @staticmethod
    def total_debt():
        result = 0
        for personal_account in PersonalAccount.objects.all():
            balance = personal_account.balance
            if balance < 0:
                result += balance
        return result

    @staticmethod
    def total_balance():
        result = 0
        for personal_account in PersonalAccount.objects.all():
            balance = personal_account.balance
            if balance > 0:
                result += balance
        return result

    class StatusName(models.TextChoices):
        ACTIVE = 'Активен', 'Активен'
        DISABLED = 'Неактивен', 'Неактивен'

    status = models.CharField(choices=StatusName.choices, max_length=9)
    apartment = models.OneToOneField(Apartment, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.number
