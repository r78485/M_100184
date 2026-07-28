import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from apps.users.models import StudentAdmission

print("Initial Student Count:", StudentAdmission.objects.count())

try:
    s = StudentAdmission.objects.create(
        student_name_bn="পরীক্ষামূলক ছাত্র",
        student_name_en="Test Student",
        desired_class="Class 6",
        mobile="01700000000",
        status="Approved"
    )
    print("Successfully created student ID:", s.id, "Admission No:", s.admission_no)
    print("New Student Count:", StudentAdmission.objects.count())
except Exception as e:
    import traceback
    print("Error creating student:", e)
    traceback.print_exc()
