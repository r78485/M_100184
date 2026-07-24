#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

# Create default superusers on deployment
python manage.py shell -c "
from apps.users.models import User
for uname, uemail in [('M_100184', 'school100184@gmail.com'), ('admin', 'admin@example.com')]:
    u, created = User.objects.get_or_create(username=uname, defaults={'email': uemail, 'role': 'ADMIN', 'is_staff': True, 'is_superuser': True, 'is_active': True})
    u.set_password('admin1234')
    u.email = uemail
    u.role = 'ADMIN'
    u.is_staff = True
    u.is_superuser = True
    u.is_active = True
    u.save()
    print(f'Superuser {uname} synchronized successfully')
"


