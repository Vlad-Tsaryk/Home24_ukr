import datetime

from django.core.management.base import BaseCommand
import random
from faker import Faker

from admin_personal_account.models import PersonalAccount
from admin_receipt.models import Receipt, ReceiptService
from admin_tariff.models import TariffService


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many transactions generate')
        parser.add_argument('month', type=int, help='month of receipt creation')

    def handle(self, *args, **options):
        fake = Faker('uk_UA')
        personal_accounts = PersonalAccount.objects.filter(apartment__isnull=False).select_related('apartment__tariff')
        receipt_last_pk = 1
        if Receipt.objects.exists():
            receipt_last_pk = Receipt.objects.first().pk + 1
        for index in range(options['number']):
            personal_account = random.choice(personal_accounts)
            date = datetime.date.today()
            set_date = datetime.date(day=date.day, month=options['month'], year=date.year)
            receipt = Receipt.objects.create(
                personal_account=personal_account,
                tariff=personal_account.apartment.tariff,
                is_complete=fake.boolean(chance_of_getting_true=75),
                date=set_date,
                status=random.choice(Receipt.StatusName.values),
                period_start=set_date,
                period_end=set_date,
                number=str(receipt_last_pk + index).zfill(11)
            )
            total_price = 0
            tariff_services = TariffService.objects.filter(tariff=personal_account.apartment.tariff)
            for tariff_service in tariff_services:
                price_unit = tariff_service.price
                consumption = round(random.uniform(1, 30), 1)
                ReceiptService.objects.create(
                    receipt=receipt,
                    service=tariff_service.service,
                    consumption=round(random.uniform(1, 30), 1),
                    price_unit=tariff_service.price
                )
                total_price += price_unit * consumption
            receipt.total_price = total_price
            receipt.save()
        print(f'Receipt created: {options["number"]}')
