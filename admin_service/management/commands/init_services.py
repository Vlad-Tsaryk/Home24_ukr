import random

from django.core.management.base import BaseCommand

from admin_service.models import Unit, Service


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Unit.objects.exists() and not Service.objects.exists():
            unit_names = ['г/кал', 'kW⋅h', 'm3']
            service_names = ['Тепло', 'Электроэнергия', 'Газ', 'Хол.вода', 'Гор.вода']
            unit = None
            for unit_name, service_name in zip(unit_names, service_names):
                unit = Unit.objects.create(
                    name=unit_name
                )
                Service.objects.create(
                    name=service_name,
                    is_counter=True,
                    unit=unit
                )

            for service_name in service_names[-2:]:
                Service.objects.create(
                    name=service_name,
                    is_counter=True,
                    unit=unit
                )
