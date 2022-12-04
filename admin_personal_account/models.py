from django.db import models
from admin_apartment.models import Apartment


# Create your models here.
class PersonalAccount(models.Model):
    class StatusName(models.TextChoices):
        ACTIVE = 'Активен', 'Активен'
        DISABLED = 'Неактивен', 'Неактивен'
    status = models.CharField(choices=StatusName.choices, max_length=9)
    apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True)
