#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# Create default superuser on deployment if not existing
python manage.py shell -c "
from apps.users.models import User
if not User.objects.filter(username='M_100184').exists():
    u = User.objects.create_superuser('M_100184', 'school100184@gmail.com', 'admin1234', role='ADMIN')
    print('Superuser M_100184 created successfully')
if not User.objects.filter(username='admin').exists():
    u = User.objects.create_superuser('admin', 'admin@example.com', 'admin1234', role='ADMIN')
    print('Superuser admin created successfully')
"

