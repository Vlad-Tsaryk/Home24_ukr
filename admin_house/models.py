from django.db import models
from users.models import User


# Create your models here.
class House(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=50, unique=True)
    image1 = models.ImageField(upload_to='houses')
    image2 = models.ImageField(upload_to='houses')
    image3 = models.ImageField(upload_to='houses')
    image4 = models.ImageField(upload_to='houses')
    image5 = models.ImageField(upload_to='houses')
    users = models.ManyToManyField(User, through='HouseUser')


class Section(models.Model):
    name = models.CharField(max_length=50)
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class Floor(models.Model):
    name = models.CharField(max_length=50)
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class HouseUser(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
