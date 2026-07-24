from django.db import models
from django.conf import settings
from apps.academics.models import StudentProfile

class StudentAttendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Present (Biometric)', 'Present (Biometric)'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Personal Leave', 'Personal Leave'),
        ('Holiday', 'Holiday'),
        ('Pending', 'Pending'),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.date} - {self.status}"

class TeacherAttendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Present (Biometric)', 'Present (Biometric)'),
        ('Absent', 'Absent'),
        ('Casual Leave', 'Casual Leave'),
        ('Special Leave', 'Special Leave'),
        ('Holiday', 'Holiday'),
        ('Pending', 'Pending'),
    )
    # Teachers are just Users with role='TEACHER' in apps.users.models
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_attendances', limit_choices_to={'role': 'TEACHER'})
    date = models.DateField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        unique_together = ('teacher', 'date')

    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.date} - {self.status}"
