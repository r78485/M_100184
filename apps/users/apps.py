from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        try:
            from django.core.management import call_command
            call_command('makemigrations', 'users', interactive=False)
            call_command('migrate', interactive=False)
        except Exception as e:
            print("Auto-migration note:", e)

