from django.apps import AppConfig
import sys

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        if 'migrate' not in sys.argv and 'makemigrations' not in sys.argv:
            try:
                from django.core.management import call_command
                from django.db import connection
                tables = connection.introspection.table_names()
                if 'django_session' not in tables or 'users_user' not in tables:
                    call_command('migrate', interactive=False)
            except Exception:
                pass
