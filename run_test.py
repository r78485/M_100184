import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.core.management import call_command
try:
    call_command('migrate', interactive=False)
    print("Migrate completed successfully!")
except Exception as e:
    print("Migration exception:", e)
