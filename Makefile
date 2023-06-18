start:
	python3 manage.py migrate
	python3 manage.py collectstatic --no-input
	gunicorn home24.wsgi:application --bind 0.0.0.0:8000

init:
	python3 manage.py migrate
	python3 manage.py collectstatic --no-input
	python3 manage.py init_role
	python3 manage.py init_admin
	python3 manage.py init_website
	python3 manage.py init_purpose
	python3 manage.py init_services
	python3 manage.py init_tariffs
	python3 manage.py create_users 30
	python3 manage.py create_owners 20
	python3 manage.py create_houses 12
	python3 manage.py create_apartments 30
	python3 manage.py create_transactions 10 1
	python3 manage.py create_transactions 15 2
	python3 manage.py create_transactions 10 3
	python3 manage.py create_receipts 12 1
	python3 manage.py create_receipts 11 2
	python3 manage.py create_receipts 9 3
	python3 manage.py create_meter_values 100
	python3 manage.py create_applications 30
