from django.db import models
from django.db.models import F

from admin_apartment.models import Apartment
from users.models import User, Role


# Create your models here.
class Application(models.Model):
    class StatusName(models.TextChoices):
        NEW = 'Новое', 'Новое'
        IN_PROGRESS = 'В работе', 'В работе'
        DONE = 'Выполнено', 'Выполнено'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    master = models.ForeignKey(User, on_delete=models.PROTECT, related_name='master')
    status = models.CharField(max_length=10, choices=StatusName.choices)
    comment = models.TextField()
    description = models.TextField()
    date = models.DateField()
    date_add = models.DateTimeField(auto_now_add=True)
    time = models.TimeField()

    class Meta:
        ordering = ['-pk']
