import datetime
import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
from admin_apartment.models import Apartment
from admin_application.models import Application
from users.models import User, Role


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many applications create')

    def handle(self, *args, **options):
        def round_dt(dt, minutes):
            return datetime.datetime.min + round((dt - datetime.datetime.min) / minutes) * minutes
        fake = Faker('uk_UA')
        masters = User.objects.filter(role__role__in=[Role.RoleName.PLUMBER, Role.RoleName.ELECTRICIAN])
        apartments = Apartment.objects.filter(owner__isnull=False).select_related('owner')
        minutes = datetime.timedelta(minutes=15)
        for index in range(options['number']):
            apartment = random.choice(apartments)
            master = random.choice(masters)
            date = datetime.datetime.now() + datetime.timedelta(days=random.randrange(1, 5))
            Application.objects.create(
                owner=apartment.owner,
                apartment=apartment,
                master=master,
                master_type=master.role.role,
                status=random.choice(Application.StatusName.values),
                comment=fake.paragraph(nb_sentences=3),
                description='У мене катастрофа. Допоможіть!',
                date=date.date(),
                time=round_dt(date, minutes).time(),
            )
