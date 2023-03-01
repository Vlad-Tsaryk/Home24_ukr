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
            personal_account_last_pk = PersonalAccount.objects.last().pk + 1
        for index in range(options['number']):
            try:
                random_house = random.choice(houses)
                sections = Section.objects.filter(house=random_house)
                floors = Floor.objects.filter(house=random_house)
                if sections:
                    section = random.choice(sections)
                else:
                    random_house = random.choice(houses)
                    sections = Section.objects.filter(house=random_house)
                    floors = Floor.objects.filter(house=random_house)
                    section = random.choice(sections)
                apartment = Apartment.objects.create(
                    number=random.randrange(1, 1000),
                    area=random.randrange(50, 300, 5),
                    house=random_house,
                    section=section,
                    floor=random.choice(floors),
                    owner=random.choice(owners),
                    tariff=random.choice(tariffs)
                )
                print(f"Apartment{apartment.number} create")
                number = str(personal_account_last_pk+index).zfill(11)
                PersonalAccount.objects.create(
                    number=number,
                    apartment=apartment,
                    status=PersonalAccount.StatusName.ACTIVE
                )
                print(f"PersonalAccount {number} create")
            except IntegrityError:
                continue
