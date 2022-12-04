from django.db import models
from admin_house.models import House, Section, Floor
from users.models import User
from admin_tariff.models import Tariff


# Create your models here.
class Apartment(models.Model):
    number = models.IntegerField(unique=True)
    area = models.IntegerField()
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='houses')
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    floor = models.ForeignKey(Floor, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    tariff = models.ForeignKey(Tariff, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Квартира №{self.number}, {self.house}'
