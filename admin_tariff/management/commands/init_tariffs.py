import random

from django.core.management.base import BaseCommand

from admin_service.models import Service
from admin_tariff.models import Tariff, TariffService


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Tariff.objects.exists():
            tariff_names = ["Економ", "Vip", "Комфорт", "Комерційний"]
            services = Service.objects.all()
            for tariff_name in tariff_names:
                tariff = Tariff.objects.create(
                    name=tariff_name,
                    description=tariff_name,
                )
                services_list = []
                for _ in range(random.randrange(1, services.count())):
                    service = random.choice(services)
                    if service not in services_list:
                        services_list.append(service)
                        TariffService.objects.create(
                            tariff=tariff,
                            service=service,
                            price=round(random.uniform(1, 50), 2),
                        )
