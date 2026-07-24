from django.db import models
from authentication.models import User

class Class(models.fields.Model):
    name = models.CharField(max_length=50) # e.g., Class 9

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=10) # e.g., A, B
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.assigned_class.name} - Section {self.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.assigned_class.name})"

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Teacher'})
    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'Student'})
    roll_number = models.CharField(max_length=20, unique=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.roll_number})"
