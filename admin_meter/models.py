from django.db import models
from admin_apartment.models import Apartment
from admin_service.models import Service


# Create your models here.
class Meter(models.Model):
    class StatusName(models.TextChoices):
        NEW = 'Новое', 'Новое'
        CLARIFIED = 'Учтено', 'Учтено'
        CLARIFIED_PAID = 'Учтено и оплачено', 'Учтено и оплачено'
        ZERO = 'Нулевое', 'Нулевое'

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    number = models.CharField(max_length=50, unique=True)
    value = models.FloatField()
    date = models.DateField()
    status = models.CharField(choices=StatusName.choices, max_length=20)

    class Meta:
        ordering = ['pk']
