from django.core.management.base import BaseCommand
from users.models import Role
from admin_purpose.models import PaymentDetails
from faker import Faker


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(2):
            Role.objects.create(
                role=Role.RoleName.choices[_][1],
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
                payment_details=True,
            )
        for _ in range(2, 6):
            Role.objects.create(
                role=Role.RoleName.choices[_][1],
                statistics=fake.boolean(),
                transaction=fake.boolean(),
                personal_account=fake.boolean(),
                apartment=fake.boolean(),
                owners=fake.boolean(),
                house=fake.boolean(),
                message=fake.boolean(),
                application=fake.boolean(),
                counter=fake.boolean(),
                website=fake.boolean(),
                services=fake.boolean(),
                roles=fake.boolean(),
                users=fake.boolean(),
                payment_details=fake.boolean(),
            )
        PaymentDetails.objects.create(name="Home24", info="Welcome to Home24")
