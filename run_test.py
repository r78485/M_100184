import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from apps.users.views import get_realtime_dashboard_data

data = get_realtime_dashboard_data()
print("Realtime Dashboard Data:")
for k, v in data.items():
    print(f" - {k}: {v}")

