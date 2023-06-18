#!/bin/sh
python manage.py init_website
python manage.py init_purpose
python manage.py init_services
python manage.py init_tariffs
python manage.py create_users 30
python manage.py create_owners 20
python manage.py create_houses 12
python manage.py create_apartments 30
python manage.py create_transactions 10 1
python manage.py create_transactions 15 2
python manage.py create_transactions 10 3
python manage.py create_receipts 12 1
python manage.py create_receipts 11 2
python manage.py create_receipts 9 3
python manage.py create_meter_values 100
python manage.py create_applications 30
exec "$@"
