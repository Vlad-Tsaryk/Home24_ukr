from django.db import models
from admin_house.models import House, Section, Floor
from users.models import User
from admin_tariff.models import Tariff


# Create your models here.
class Apartment(models.Model):
    number = models.IntegerField(unique=True)
    area = models.IntegerField()
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    floor = models.ForeignKey(Floor, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tariff = models.ForeignKey(Tariff, null=True, on_delete=models.SET_NULL)
