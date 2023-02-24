from django.db import models

from admin_apartment.models import Apartment
from admin_receipt.models import Receipt


# Create your models here.
class PersonalAccount(models.Model):
    @property
    def balance(self):
        try:
            transaction_sum = self.transaction_set.all().filter(is_complete=True) \
                                  .aggregate(models.Sum('sum'))['sum__sum'] or 0
            receipt_sum = self.apartment.receipt_set.all().exclude(status=Receipt.StatusName.PAID) \
                              .filter(is_complete=True) \
                              .aggregate(total_price=models.Sum('total_price'))['total_price'] or 0
            return transaction_sum - receipt_sum
        except:
            return 0

    @staticmethod
    def owner_has_debt(owner_id):
        balance = 0
        for personal_account in PersonalAccount.objects.select_related('apartment').filter(apartment__owner=owner_id):
            balance += personal_account.balance
        if balance >= 0:
            return False
        else:
            return True

    @staticmethod
    def total_debt():
        result = 0
        for personal_account in PersonalAccount.objects.select_related('apartment').all():
            balance = personal_account.balance
            if balance < 0:
                result += balance
        return result

    @staticmethod
    def total_balance():
        result = 0
        for personal_account in PersonalAccount.objects.select_related('apartment').all():
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
