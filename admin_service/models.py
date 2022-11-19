from django.db import models


# Create your models here.
class Unit(models.Model):
    def used_in_service(self):
        return self.service_set.exists()

    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': "Единица измерения с таким именем уже существует!"})

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': "Услуга с таким именем уже существует!"})
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True)
    is_counter = models.BooleanField(default=False)

    def in_usage(self):
        if self.tariffservice_set.exists():
            return 'Услуга используется в тарифах'
        else:
            return False

    def __str__(self):
        return self.name
