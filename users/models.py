from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image


# Create your models here.
class Role(models.Model):
    class RoleName(models.TextChoices):
        DIRECTOR = 'Директор', 'Директор'
        MANAGER = 'Керуючий', 'Керуючий'
        ACCOUNTANT = 'Бухгалтер', 'Бухгалтер'
        ELECTRICIAN = 'Електрик', 'Електрик'
        PLUMBER = 'Сантехнік', 'Сантехнік'
        OWNER = 'Власник квартири', 'Власник квартири'

    role = models.CharField(choices=RoleName.choices, max_length=20)
    statistics = models.BooleanField()
    transactions = models.BooleanField()
    receipts = models.BooleanField()
    personal_accounts = models.BooleanField()
    apartments = models.BooleanField()
    owners = models.BooleanField()
    houses = models.BooleanField()
    messages = models.BooleanField()
    applications = models.BooleanField()
    meters = models.BooleanField()
    website = models.BooleanField()
    services = models.BooleanField()
    tariffs = models.BooleanField()
    roles = models.BooleanField()
    users = models.BooleanField()
    payment_details = models.BooleanField()

    def __str__(self):
        return self.role


class User(AbstractUser):
    class StatusName(models.TextChoices):
        NEW = 'Новий', 'Новий'
        ACTIVE = 'Активний', 'Активний'
        DISABLED = 'Вимкнений', 'Вимкнений'

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.EmailField(unique=True, error_messages={
        'unique': "Користувач із таким логіном вже існує!"})
    phone = PhoneNumberField()
    birth_date = models.DateField(blank=True, null=True)
    status = models.CharField(choices=StatusName.choices, max_length=10)
    viber = PhoneNumberField(blank=True)
    telegram = models.CharField(max_length=32)
    notes = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='users')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    uid = models.CharField(max_length=10, null=True, unique=True)

    def __str__(self):
        return ' '.join((self.first_name, self.middle_name, self.last_name))

    def get_apartments(self):
        user = User.objects.get(id=self.pk)
        return user.apartment_set.select_related('house')

    @staticmethod
    def get_owners():
        return User.objects.filter(role=Role.objects.get(role=Role.RoleName.OWNER))

    def get_new_users(self):
        return User.objects.filter(status=self.StatusName.NEW)

    def get_status_label_color(self):
        colors = {
            'Активний': 'label-success',
            'Вимкнений': 'label-danger',
            'Новий': 'label-warning',
        }
        return colors[self.status]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_image:
            if self.profile_image.size != (160, 160):
                image = Image.open(self.profile_image.path)
                image = image.resize((160, 160))
                image.save(self.profile_image.path)

    class Meta:
        ordering = ['-date_joined']
