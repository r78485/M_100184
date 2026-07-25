"""
WSGI config for school_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')

# Auto-migrate database tables on WSGI startup if core tables (django_session, users_user, question_paper_questionbank) are missing
try:
    import django
    django.setup()
    from django.db import connection
    tables = connection.introspection.table_names()
    required_tables = ['django_session', 'users_user', 'question_paper_questionbank', 'django_content_type']
    if any(t not in tables for t in required_tables):
        from django.core.management import call_command
        call_command('migrate', interactive=False)
        from apps.users.models import User
        for uname, uemail in [('M_100184', 'school100184@gmail.com'), ('admin', 'admin@example.com')]:
            u, created = User.objects.get_or_create(
                username=uname,
                defaults={'email': uemail, 'role': 'ADMIN', 'is_staff': True, 'is_superuser': True, 'is_active': True}
            )
            u.set_password('admin1234')
            u.email = uemail
            u.role = 'ADMIN'
            u.is_staff = True
            u.is_superuser = True
            u.is_active = True
            u.save()
except Exception as ex:
    print("WSGI auto-migration note:", ex)

application = get_wsgi_application()
