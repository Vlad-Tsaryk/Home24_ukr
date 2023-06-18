from admin_apartment.models import Apartment
from admin_house.models import House, Floor, Section
from users.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sender"
    )
    receivers = models.ManyToManyField(User)
    house = models.ForeignKey(House, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=78)
    text = models.TextField()
    is_read = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)

    @property
    def get_receiver_label(self):
        if (
            not (self.house or self.section or self.apartment or self.floor)
            and self.receivers.count() == 1
        ):
            return str(self.receivers.first())
        if self.house:
            return (
                f'{self.house} {self.section or ""} '
                f'{self.floor or ""} {self.apartment or ""}'
            )
        else:
            return "Всім"
