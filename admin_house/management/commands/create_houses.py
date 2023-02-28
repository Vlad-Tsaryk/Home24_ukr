import random

from django.core.management.base import BaseCommand
from faker import Faker

from admin_house.models import House, Section, Floor

from users.models import User, Role


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many houses create')

    def handle(self, *args, **options):
        fake = Faker()
        fake_uk = Faker('uk_UA')
        users = User.objects.exclude(role__role=Role.RoleName.OWNER)
        for _ in range(options['number']):
            name = fake.company()
            while len(name) > 50:
                name = fake.company()
            address = fake_uk.address()
            while len(address) > 50:
                address = fake_uk.address()
            house = House.objects.create(
                name=f'ЖК "{name}" ',
                address=address,
                image1=f'static_kit/houses/{random.randrange(1, 14)}.jpg',
                image2=f'static_kit/houses/{random.randrange(1, 14)}.jpg',
                image3=f'static_kit/houses/{random.randrange(1, 14)}.jpg',
                image4=f'static_kit/houses/{random.randrange(1, 14)}.jpg',
                image5=f'static_kit/houses/{random.randrange(1, 14)}.jpg',
            )
            for _ in range(random.randrange(1, 6)):
                house.users.add(random.choice(users))

            for index in range(random.randrange(1, 6)):
                Section.objects.create(
                    name=f'Секция {index + 1}',
                    house=house
                )
                Floor.objects.create(
                    name=f'Этаж {index + 1}',
                    house=house
                )
