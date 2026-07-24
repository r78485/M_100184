import os
import sys
import django

# Setup django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from apps.transcripts.models import InstitutionProfile, GradingScale, Student, StudentResult
from datetime import date

def seed_data():
    # 1. Create Institution
    inst, created = InstitutionProfile.objects.get_or_create(
        eiin="100184",
        defaults={
            'name_en': 'GOVT. HIGH SCHOOL, NARAYANGANJ',
            'name_bn': 'সরকারি উচ্চ বিদ্যালয়, নারায়ণগঞ্জ',
            'board_or_authority': 'Directorate of Secondary and Higher Education'
        }
    )

    # 2. Create Grading Scales
    scales = [
        (80, 100, 'A+', 5.00),
        (70, 79, 'A', 4.00),
        (60, 69, 'A-', 3.50),
        (50, 59, 'B', 3.00),
        (40, 49, 'C', 2.00),
        (0, 39, 'F', 0.00),
    ]
    for mark_from, mark_to, grade, point in scales:
        GradingScale.objects.get_or_create(
            mark_from=mark_from,
            mark_to=mark_to,
            defaults={'letter_grade': grade, 'grade_point': point}
        )

    # 3. Create Dummy Students
    student_ids = ["1", "S-501", "S-502", "S-503"]
    names = ["Test Student", "Arif Rahman", "Jannatul Ferdous", "Rakib Hasan"]

    for sid, name in zip(student_ids, names):
        stu, created = Student.objects.get_or_create(
            student_id=sid,
            defaults={
                'roll_no': f'100{sid}',
                'registration_no': f'20260{sid}',
                'session': '2025-2026',
                'full_name': name,
                'father_name': 'Father Name',
                'mother_name': 'Mother Name',
                'exam_name': 'Annual Examination',
                'group_or_subject': 'Science',
                'dob': date(2010, 1, 1)
            }
        )

        if created:
            # 4. Create Results for the student
            subjects = [
                ('101', 'Bengali', 85),
                ('107', 'English', 82),
                ('109', 'Mathematics', 95),
                ('127', 'Science', 88),
            ]
            for code, sname, marks in subjects:
                StudentResult.objects.create(
                    student=stu,
                    subject_code=code,
                    subject_name=sname,
                    obtained_marks=marks
                )

    print("Successfully seeded database with dummy student and grading data.")

if __name__ == '__main__':
    seed_data()
