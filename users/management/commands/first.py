from django.core.management.base import BaseCommand
from datetime import datetime
from users.models import Role
from faker import Faker


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(6):
            Role.objects.create(
                role=Role.CHOICES_role[_],
                statistics=True,
                transaction=True,
                personal_account=True,
                apartment=True,
                owners=True,
                house=True,
                message=True,
                application=True,
                counter=True,
                website=True,
                services=True,
                roles=True,
                users=True,
                payment_details=True
            )
