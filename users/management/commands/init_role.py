from django.core.management.base import BaseCommand
from users.models import Role


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not Role.objects.exists():
            for director_manger in Role.RoleName.values[:2]:
                Role.objects.create(role=director_manger,
                                    statistics=True,
                                    transactions=True,
                                    receipts=True,
                                    personal_accounts=True,
                                    apartments=True,
                                    owners=True,
                                    houses=True,
                                    messages=True,
                                    applications=True,
                                    meters=True,
                                    website=True,
                                    services=True,
                                    tariffs=True,
                                    roles=True,
                                    users=True,
                                    payment_details=True)

            for electrician_plumber in Role.RoleName.values[:-2]:
                Role.objects.create(role=electrician_plumber,
                                    statistics=False,
                                    transactions=False,
                                    receipts=False,
                                    personal_accounts=False,
                                    apartments=False,
                                    owners=False,
                                    houses=False,
                                    messages=True,
                                    applications=True,
                                    meters=False,
                                    website=False,
                                    services=False,
                                    tariffs=False,
                                    roles=False,
                                    users=False,
                                    payment_details=False)

            Role.objects.create(role=Role.RoleName.ACCOUNTANT,
                                statistics=True,
                                transactions=True,
                                receipts=True,
                                personal_accounts=True,
                                apartments=True,
                                owners=False,
                                houses=True,
                                messages=True,
                                applications=True,
                                meters=True,
                                website=False,
                                services=True,
                                tariffs=True,
                                roles=False,
                                users=False,
                                payment_details=True)

            Role.objects.create(role=Role.RoleName.OWNER,
                                statistics=False,
                                transactions=False,
                                receipts=False,
                                personal_accounts=False,
                                apartments=False,
                                owners=False,
                                houses=False,
                                messages=False,
                                applications=False,
                                meters=False,
                                website=False,
                                services=False,
                                tariffs=False,
                                roles=False,
                                users=False,
                                payment_details=False)
