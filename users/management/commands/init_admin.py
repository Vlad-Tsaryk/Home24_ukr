from django.core.management.base import BaseCommand
from users.models import User, Role
from faker import Faker
from random import choice
from phonenumber_field.phonenumber import PhoneNumber


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()

        if User.objects.count() == 0:
            username = 'admin'
            email = 'admin@admin.com'
            password = 'admin'
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(
                username=email,
                first_name='Admin',
                last_name='Admin',
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
            print('Admin already initialize')
