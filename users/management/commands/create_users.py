from django.core.management.base import BaseCommand
from users.models import User, Role
import random
from faker import Faker
from phonenumber_field.phonenumber import PhoneNumber


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many sessions generate')

    def handle(self, *args, **options):
        fake = Faker('uk_UA')
        for _ in range(int(options['number']/2)):
            user = User.objects.create_user(
                first_name=fake.first_name_female(),
                last_name=fake.last_name_female(),
                phone=PhoneNumber.from_string('+38 (073) 242-58-82', region="UA"),
                username=fake.email(),
                password='Admin12345',
                status=random.choice(User.StatusName.values),
                role=Role.objects.get(role=random.choice(Role.RoleName.values[1:5])),
                profile_image=f'static_kit/users/2.png'
            )
            print('User **' + user.username + '** successfully create')
        for _ in range(int(options['number']/2)):
            user = User.objects.create_user(
                first_name=fake.first_name_male(),
                last_name=fake.last_name_male(),
                phone=PhoneNumber.from_string('+38 (073) 242-58-82', region="UA"),
                username=fake.email(),
                password='Admin12345',
                status=random.choice(User.StatusName.values),
                role=Role.objects.get(role=random.choice(Role.RoleName.values[1:5])),
                profile_image=f'static_kit/users/1.png'
            )
            print('User **' + user.username + '** successfully create')
