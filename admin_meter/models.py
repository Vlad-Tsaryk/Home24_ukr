from django.db import models
from admin_apartment.models import Apartment
from admin_service.models import Service


# Create your models here.
class Meter(models.Model):
    class StatusName(models.TextChoices):
        NEW = 'Нове', 'Нове'
        CLARIFIED = 'Враховано', 'Враховано'
        CLARIFIED_PAID = 'Враховано та оплачено', 'Враховано та оплачено'
        ZERO = 'Нульове', 'Нульове'

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    number = models.CharField(max_length=50, unique=True)
    value = models.FloatField()
    date = models.DateField()
    status = models.CharField(choices=StatusName.choices, max_length=21)

    class Meta:
        ordering = ['pk']
