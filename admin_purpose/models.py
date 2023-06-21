from django.db import models


# Create your models here.
class Purpose(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = "Надходження", "Надходження"
        OUTCOME = "Витрата", "Витрата"

    name = models.CharField(
        max_length=50,
        unique=True,
        error_messages={"unique": "Стаття з такою назвою вже існує!"},
    )
    transaction_type = models.CharField(choices=TransactionType.choices, max_length=11)

    def __str__(self):
        return self.name


class PaymentDetails(models.Model):
    name = models.CharField(blank=True, max_length=128)
    info = models.TextField(blank=True)
