from django.core.management.base import BaseCommand
from users.models import User, Role
from faker import Faker
from random import choice
from phonenumber_field.phonenumber import PhoneNumber


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
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

            for electrician_plumber in Role.RoleName.choices[:-2]:
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

        if User.objects.count() == 0:
            username = 'admin'
            email = 'admin@admin.com'
            password = 'admin'
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(
                username=email,
                first_name=username,
                middle_name=username,
                last_name=username,
                phone=PhoneNumber.from_string('+38 (073) 111-11-11', region="UA"),
                viber=PhoneNumber.from_string('+38 (073) 111-11-11', region="UA"),
                telegram='@' + 'admin',
                birth_date=fake.date_of_birth(minimum_age=16, maximum_age=55),
                password=password,
                status=choice(User.StatusName.choices)[0],
                role=Role.objects.get(role=Role.RoleName.DIRECTOR),
                notes=fake.text(max_nb_chars=500),
                profile_image=f'static_kit/users/admin.png'
            )
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
