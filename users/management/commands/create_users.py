from django.core.management.base import BaseCommand
from users.models import User, Role
import random
from faker import Faker
from phonenumber_field.phonenumber import PhoneNumber


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many sessions generate')

    def handle(self, *args, **options):
        fake = Faker('ru_RU')
        for _ in range(options['number']):
            user = User.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=PhoneNumber.from_string('+38 (073) 242-58-82', region="UA"),
                username=fake.email(),
                password='Admin12345',
                status=random.choice(User.StatusName.choices),
                role=Role.objects.get(role=random.choice(Role.RoleName.values[1:5])),
                profile_image=f'static_kit/users/{random.randrange(1, 3)}.png'
            )
            print('User **' + user.telegram + '** successfully create')
