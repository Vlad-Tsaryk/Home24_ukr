from django.db import models


# Create your models here.
class Unit(models.Model):
    def used_in_service(self):
        return self.service_set.exists()

    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': "Одиниця виміру з таким ім'ям вже існує!"})

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': "Послуга з такою назвою вже існує!"})
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True)
    is_counter = models.BooleanField(default=False)

    def in_usage(self):
        if self.tariffservice_set.exists():
            return 'Послуга використовується у тарифах'
        else:
            return False

    def __str__(self):
        return self.name
