from django.db import models


# Create your models here.
class Purpose(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = 'Приход', 'Приход'
        OUTCOME = 'Расход', 'Расход'

    name = models.CharField(max_length=50, unique=True, error_messages={
                                                           'unique': "Статья с таким именем уже существует!"})
    transaction_type = models.CharField(choices=TransactionType.choices, max_length=6)


class PaymentDetails(models.Model):
    name = models.CharField(blank=True, max_length=128)
    info = models.TextField(blank=True)


