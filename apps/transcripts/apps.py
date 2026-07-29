from django.apps import AppConfig

class TranscriptsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.transcripts'

    def ready(self):
        try:
            from django.core.management import call_command
            call_command('migrate', 'transcripts', interactive=False)
        except Exception as e:
            pass

