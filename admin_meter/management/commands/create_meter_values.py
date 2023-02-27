import datetime
from django.core.management.base import BaseCommand
import random
from admin_apartment.models import Apartment
from admin_meter.models import Meter
from admin_service.models import Service


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many meter values generate')

    def handle(self, *args, **options):
        services = Service.objects.filter(is_counter=True)
        apartments = Apartment.objects.all()
        meter_last_pk = 1
        if Meter.objects.exists():
            meter_last_pk = Meter.objects.last().pk + 1
        for index in range(options['number']):
            apartment = random.choice(apartments)
            service = random.choice(services)
            try:
                value = Meter.objects.filter(apartment=apartment, service=service).last().value
            except:
                value = 0
            Meter.objects.create(
                apartment=apartment,
                service=service,
                number=str(meter_last_pk + index).zfill(11),
                value=value + random.randrange(5, 50),
                date=datetime.date.today(),
                status=random.choice(Meter.StatusName.values)
            )
