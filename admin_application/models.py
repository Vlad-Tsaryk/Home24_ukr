from django.db import models

from admin_apartment.models import Apartment
from users.models import User, Role


# Create your models here.
class Application(models.Model):
    class StatusName(models.TextChoices):
        NEW = 'Новое', 'Новое'
        IN_PROGRESS = 'В работе', 'В работе'
        DONE = 'Выполнено', 'Выполнено'

    class MasterType(models.TextChoices):
        ANY = 'Любой специалист', 'Любой специалист'
        PLUMBER = 'Сантехник', 'Сантехник'
        ELECTRICIAN = 'Электрик', 'Электрик'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    master = models.ForeignKey(User, on_delete=models.PROTECT, related_name='master', null=True)
    master_type = models.CharField(max_length=16, choices=MasterType.choices)
    status = models.CharField(max_length=10, choices=StatusName.choices)
    comment = models.TextField()
    description = models.TextField()
    date = models.DateField()
    date_add = models.DateTimeField(auto_now_add=True)
    time = models.TimeField()

    class Meta:
        ordering = ['-pk']
