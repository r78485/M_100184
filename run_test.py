import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from apps.users.models import Employee
from django.db import connection

tables = connection.introspection.table_names()
print("Existing database tables:", len(tables))

if 'users_employee' not in tables:
    print("Creating users_employee table...")
    with connection.schema_editor() as editor:
        editor.create_model(Employee)
    print("Table created successfully!")

print("Current Employee Count in DB:", Employee.objects.count())

