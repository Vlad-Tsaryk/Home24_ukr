from django.db import models


# Create your models here.
class Unit(models.Model):
    def used_in_service(self):
        return self.service_set.exists()

    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': "Единица измерения с таким именем уже существует!"})


class Service(models.Model):
    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': "Услуга с таким именем уже существует!"})
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True)
    is_counter = models.BooleanField(default=False)
