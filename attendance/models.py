from django.db import models
from core.models import Section, StudentProfile, TeacherProfile

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Present (Biometric)', 'Present (Biometric)'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Personal Leave', 'Personal Leave'),
        ('Holiday', 'Holiday'),
        ('Pending', 'Pending'),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"

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
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        unique_together = ('teacher', 'date')

    def __str__(self):
        return f"{self.teacher.user.username} - {self.date} - {self.status}"
