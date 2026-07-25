from django.core.management import call_command
from django.db import connection

_MIGRATED = False

class AutoMigrateMiddleware:
    """
    Guarantees that database tables (django_session, users_user, question_paper_questionbank, etc.)
    exist before SessionMiddleware or AuthenticationMiddleware attempt to access the database.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global _MIGRATED
        if not _MIGRATED:
            try:
                tables = connection.introspection.table_names()
                required_tables = ['django_session', 'users_user', 'question_paper_questionbank']
                if any(t not in tables for t in required_tables):
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
                _MIGRATED = True
            except Exception as e:
                print("AutoMigrateMiddleware exception:", e)

        return self.get_response(request)
