import datetime

from django.core.management.base import BaseCommand
import random
from faker import Faker

from admin_personal_account.models import PersonalAccount
from admin_purpose.models import Purpose
from admin_transaction.models import Transaction
from users.models import User, Role


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("number", type=int, help="how many transactions generate")
        parser.add_argument("month", type=int, help="month of receipt creation")

    def handle(self, *args, **options):
        fake = Faker("uk_UA")
        date = datetime.date.today()
        set_date = datetime.date(day=date.day, month=options["month"], year=date.year)
        managers = User.objects.filter(
            role__role__in=[
                Role.RoleName.DIRECTOR,
                Role.RoleName.MANAGER,
                Role.RoleName.ACCOUNTANT,
            ]
        )
        personal_accounts = PersonalAccount.objects.filter(
            apartment__isnull=False
        ).select_related("apartment__owner")
        purposes = Purpose.objects.all()
        transaction_last_pk = 1
        if Transaction.objects.exists():
            transaction_last_pk = Transaction.objects.first().pk + 1

        for index in range(options["number"]):
            personal_account = random.choice(personal_accounts)
            purpose = random.choice(purposes)
            if purpose.transaction_type == Purpose.TransactionType.INCOME:
                purpose_type = 1
            else:
                purpose_type = 0
            Transaction.objects.create(
                owner=personal_account.apartment.owner,
                personal_account=personal_account,
                purpose=purpose,
                manager=random.choice(managers),
                sum=random.randrange(100, 20000, 25),
                is_complete=fake.boolean(chance_of_getting_true=75),
                date=set_date,
                number=str(transaction_last_pk + index).zfill(11),
                comment="Створена транзакція",
                type=purpose_type,
            )
        print(f'Transaction created: {options["number"]}')
