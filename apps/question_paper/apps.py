from django.apps import AppConfig
import sys

class QuestionPaperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.question_paper'
    verbose_name = 'Create Question Paper Module'

    def ready(self):
        # Auto-create database tables on app startup if missing
        if 'migrate' not in sys.argv and 'makemigrations' not in sys.argv:
            try:
                from django.core.management import call_command
                from django.db import connection
                tables = connection.introspection.table_names()
                if 'question_paper_questionbank' not in tables:
                    call_command('migrate', 'question_paper', verbosity=0)
            except Exception:
                pass
