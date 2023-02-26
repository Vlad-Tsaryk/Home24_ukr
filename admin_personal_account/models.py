from django.db import models
from admin_apartment.models import Apartment
from admin_personal_account.utils import PersonalAccountBalance


# Create your models here.
class PersonalAccount(models.Model):
    @property
    def balance(self):
        return PersonalAccountBalance.balance(personal_account=self)

    @staticmethod
    def owner_has_debt(owner_id):
        balance = 0
        for personal_account in PersonalAccount.objects.filter(apartment__owner=owner_id):
            balance += personal_account.balance
        if balance >= 0:
            return False
        else:
            return True

    class StatusName(models.TextChoices):
        ACTIVE = 'Активен', 'Активен'
        DISABLED = 'Неактивен', 'Неактивен'

    status = models.CharField(choices=StatusName.choices, max_length=9)
    apartment = models.OneToOneField(Apartment, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.number
