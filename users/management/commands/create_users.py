from django.core.management.base import BaseCommand
from users.models import User, Role
import random
from faker import Faker
from phonenumber_field.phonenumber import PhoneNumber


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many sessions generate')

    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(options['number']):
            user = User.objects.create(
                first_name=fake.first_name(),
                middle_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=PhoneNumber.from_string('+38 (073) 242-58-82', region="UA"),
                viber=PhoneNumber.from_string('+38 (073) 242-58-82', region="UA"),
                telegram='@'+fake.simple_profile()['username'],
                birth_date=fake.date_of_birth(minimum_age=16, maximum_age=55),
                username=fake.email(),
                password='Home12345',
                status=random.choice(['Активен', 'Отключен', 'Новый']),
                role=Role.objects.get(role=random.choice(Role.CHOICES_role[1:5])[0]),
                notes=fake.text(max_nb_chars=500),
                profile_image=f'static_kit/users/{random.randrange(1,3)}.png'
            )
            print('User **' + user.telegram + '** successfully create')
