from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# ১. ইনস্টিটিউট সেটিংস ও ব্র্যান্ডিং (ওয়াটারমার্ক ও লোগোর জন্য)
class InstitutionProfile(models.Model):
    name_en = models.CharField(max_length=255, default="GOVT. HIGH SCHOOL, NARAYANGANJ")
    name_bn = models.CharField(max_length=255, default="সরকারি উচ্চ বিদ্যালয়, নারায়ণগঞ্জ")
    eiin = models.CharField(max_length=20, default="100184")
    board_or_authority = models.CharField(max_length=255, default="Directorate of Secondary and Higher Education")
    logo = models.ImageField(upload_to='institution/', null=True, blank=True)
    principal_signature = models.ImageField(upload_to='signatures/', null=True, blank=True)
    controller_signature = models.ImageField(upload_to='signatures/', null=True, blank=True)

    def __str__(self):
        return self.name_en

# ২. ডাইনামিক গ্রেডিং স্কেল কনফিগারেশন
class GradingScale(models.Model):
    mark_from = models.IntegerField()
    mark_to = models.IntegerField()
    letter_grade = models.CharField(max_length=5) # e.g. A+, A, A-
    grade_point = models.DecimalField(max_digits=3, decimal_places=2) # e.g. 5.00, 4.00
    remarks = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-mark_from']

# ৩. শিক্ষার্থী প্রোফাইল
class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    roll_no = models.CharField(max_length=50)
    registration_no = models.CharField(max_length=50, unique=True)
    session = models.CharField(max_length=20) # e.g. 2024-2025
    full_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    mother_name = models.CharField(max_length=200)
    exam_name = models.CharField(max_length=100, default="J.S.C / S.S.C Examination")
    group_or_subject = models.CharField(max_length=100, default="Science")
    dob = models.DateField()

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

# ৪. বিষয় ও অর্জিত নম্বর
class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject_code = models.CharField(max_length=20)
    subject_name = models.CharField(max_length=150)
    total_credit_or_marks = models.IntegerField(default=100)
    obtained_marks = models.IntegerField()

    def get_grade_info(self):
        # সফটওয়্যারের গ্রেডিং সিস্টেম অনুযায়ী অটো মার্ক্স টু পয়েন্ট ক্যালকুলেশন
        grade = GradingScale.objects.filter(
            mark_from__lte=self.obtained_marks, 
            mark_to__gte=self.obtained_marks
        ).first()
        if grade:
            return grade.letter_grade, grade.grade_point
        return 'F', 0.00
