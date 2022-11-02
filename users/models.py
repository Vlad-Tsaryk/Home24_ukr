from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Role(models.Model):
    class RoleName(models.TextChoices):
        DIRECTOR = 'Директор', 'Директор'
        ACCOUNTANT = 'Бухгалтер', 'Бухгалтер'
        MANAGER = 'Менеджер', 'Менеджер'
        ELECTRICIAN = 'Електрик', 'Електрик'
        PLUMBER = 'Сантехник', 'Сантехник'
        OWNER = 'Владелец квартиры', 'Владелец квартиры'

    role = models.CharField(choices=RoleName.choices, max_length=20)
    statistics = models.BooleanField()
    transaction = models.BooleanField()
    personal_account = models.BooleanField()
    apartment = models.BooleanField()
    owners = models.BooleanField()
    house = models.BooleanField()
    message = models.BooleanField()
    application = models.BooleanField()
    counter = models.BooleanField()
    website = models.BooleanField()
    services = models.BooleanField()
    roles = models.BooleanField()
    users = models.BooleanField()
    payment_details = models.BooleanField()


class User(AbstractUser):
    class StatusName(models.TextChoices):
        ACTIVE = 'Активен', 'Активен'
        NEW = 'Новый', 'Новый'
        DISABLED = 'Отключен', 'Отключен'

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.EmailField(unique=True)
    phone = PhoneNumberField()
    birth_date = models.DateField(blank=True, null=True)
    status = models.CharField(choices=StatusName.choices, max_length=10)
    viber = PhoneNumberField(blank=True)
    telegram = models.CharField(max_length=32)
    notes = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='users')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='receiver')
    subject = models.CharField(max_length=78)
    text = models.TextField()
    is_read = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)