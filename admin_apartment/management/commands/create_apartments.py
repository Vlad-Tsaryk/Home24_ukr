import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from admin_apartment.models import Apartment
from admin_house.models import House, Section, Floor
from admin_personal_account.models import PersonalAccount
from admin_tariff.models import Tariff

from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many apartments create')

    def handle(self, *args, **options):
        owners = User.get_owners()
        houses = House.objects.all()
        tariffs = Tariff.objects.all()
        personal_account_last_pk = 1
        if PersonalAccount.objects.exists():
            personal_account_last_pk = PersonalAccount.objects.last().pk
        for _ in range(options['number']):
            random_house = random.choice(houses)
            try:
                apartment = Apartment.objects.create(
                    number=random.randrange(1, 1000),
                    area=random.randrange(50, 300, 5),
                    house=random_house,
                    section=random.choice(Section.objects.filter(house=random_house)),
                    floor=random.choice(Floor.objects.filter(house=random_house)),
                    owner=random.choice(owners),
                    tariff=random.choice(tariffs)

                )
                PersonalAccount.objects.create(
                    number=str(personal_account_last_pk).zfill(11),
                    apartment=apartment,
                    status=PersonalAccount.StatusName.ACTIVE
                )
            except IntegrityError:
                continue
