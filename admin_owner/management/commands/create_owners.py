from django.core.management.base import BaseCommand
from users.models import User, Role
import random
from faker import Faker
from phonenumber_field.phonenumber import PhoneNumber


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='how many owners generate')

    def handle(self, *args, **options):
        male_mid_names = ['Вадимович', 'Володимирович', 'Андрійович', 'Валентинович', 'Ігоревич', 'Васильович',
                          'Вітальович', 'Юрійович', 'Степанович']
        female_mid_names = ['Олегівна', 'Ігорівна', 'Андріївна', 'Валентинівна', 'Ігорівна', 'Василівна',
                            'Віталівна', 'Максимівна', 'Вікторівна']

        fake = Faker('uk_UA')
        role = Role.objects.get(role=Role.RoleName.OWNER)
        owner_last_pk = 1
        if User.get_owners().exists():
            owner_last_pk = User.get_owners().order_by('pk').last().pk + 1
        for index in range(int(options['number'] / 2)):
            user = User.objects.create_user(
                first_name=fake.first_name_female(),
                middle_name=random.choice(female_mid_names),
                last_name=fake.last_name_female(),
                phone=PhoneNumber.from_string('+38 (073) 111-111-111', region="UA"),
                viber=PhoneNumber.from_string('+38 (073) 111-111-111', region="UA"),
                telegram='@' + fake.simple_profile()['username'],
                birth_date=fake.date_of_birth(minimum_age=16, maximum_age=55),
                username=fake.email(),
                password='Home12345',
                status=random.choice(User.StatusName.values),
                role=role,
                notes=fake.text(max_nb_chars=500),
                profile_image=f'static_kit/users/2.png',
                uid=str(owner_last_pk + index).zfill(6)
            )
            print('Owner **' + user.telegram + '** successfully create')
        owner_last_pk += int(options['number'] / 2)
        for index in range(int(options['number'] / 2)):
            user = User.objects.create_user(
                first_name=fake.first_name_male(),
                middle_name=random.choice(male_mid_names),
                last_name=fake.last_name_male(),
                phone=PhoneNumber.from_string('+38 (073) 111-111-111', region="UA"),
                viber=PhoneNumber.from_string('+38 (073) 111-111-111', region="UA"),
                telegram='@' + fake.simple_profile()['username'],
                birth_date=fake.date_of_birth(minimum_age=16, maximum_age=55),
                username=fake.email(),
                password='Home12345',
                status=random.choice(User.StatusName.values),
                role=role,
                notes=fake.text(max_nb_chars=500),
                profile_image=f'static_kit/users/1.png',
                uid=str(owner_last_pk + index).zfill(6)
            )
            print('Owner **' + user.telegram + '** successfully create')
