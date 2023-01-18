from django.db import models

from admin_apartment.models import Apartment


# Create your models here.
class PersonalAccount(models.Model):
    class StatusName(models.TextChoices):
        ACTIVE = 'Активен', 'Активен'
        DISABLED = 'Неактивен', 'Неактивен'

    status = models.CharField(choices=StatusName.choices, max_length=9)
    apartment = models.OneToOneField(Apartment, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.number

    @property
    def balance(self):
        result = self.transaction_set.all().filter(is_complete=True).aggregate(models.Sum('sum'))['sum__sum']
        if result:
            return result
        else:
            return 0
