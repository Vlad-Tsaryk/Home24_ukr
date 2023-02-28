from django.core.management.base import BaseCommand
import random
from faker import Faker

from admin_purpose.models import Purpose, PaymentDetails


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Purpose.objects.exists():
            purpose_names = ['Вывоз мусора', 'Погашение квитанции', 'Прочий приход', 'Перевод']
            for purpose_name in purpose_names[:2]:
                Purpose.objects.create(
                        name=purpose_name,
                        transaction_type=Purpose.TransactionType.OUTCOME
                )
            for purpose_name in purpose_names[-2:]:
                Purpose.objects.create(
                        name=purpose_name,
                        transaction_type=Purpose.TransactionType.INCOME
                )
        if not PaymentDetails.objects.exists():
            faker = Faker()
            PaymentDetails.objects.create(
                name=faker.company(),
                info=faker.company()
            )

