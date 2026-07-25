from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        TEACHER = 'TEACHER', 'Teacher'
        STUDENT = 'STUDENT', 'Student'
        
    role = models.CharField(
        max_length=10, 
        choices=Roles.choices, 
        default=Roles.STUDENT
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)

class StudentAdmission(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'অপেক্ষমাণ / Pending'),
        ('Approved', 'অনুমোদিত / Approved'),
    ]

    # Basic Information / মৌলিক তথ্য
    student_name_bn = models.CharField(max_length=200, verbose_name="নাম (বাংলা)")
    student_name_en = models.CharField(max_length=200, verbose_name="Name (English)", blank=True, default="")
    dob = models.DateField(verbose_name="জন্ম তারিখ / Date of Birth", null=True, blank=True)
    birth_reg_no = models.CharField(max_length=50, verbose_name="জন্ম নিবন্ধন নম্বর / Birth Reg No", blank=True, default="")
    gender = models.CharField(max_length=20, choices=[('Boy', 'ছেলে'), ('Girl', 'মেয়ে'), ('Other', 'অন্যান্য')], verbose_name="লিঙ্গ / Gender", default="Boy")
    mobile = models.CharField(max_length=15, verbose_name="মোবাইল নম্বর / Mobile", blank=True, default="")
    re_mobile = models.CharField(max_length=15, verbose_name="মোবাইল নম্বর নিশ্চিত করুন", blank=True, default="")

    # Parents Information / পিতা-মাতার তথ্য
    father_name = models.CharField(max_length=200, verbose_name="পিতার নাম / Father's Name", blank=True, default="")
    father_nid = models.CharField(max_length=50, verbose_name="পিতার এনআইডি / Father NID", blank=True, default="")
    father_dob = models.DateField(verbose_name="পিতার জন্ম তারিখ / Father DOB", null=True, blank=True)
    father_occupation = models.CharField(max_length=100, verbose_name="পিতার পেশা / Father Occupation", blank=True, default="")

    mother_name = models.CharField(max_length=200, verbose_name="মাতার নাম / Mother's Name", blank=True, default="")
    mother_nid = models.CharField(max_length=50, verbose_name="মাতার এনআইডি / Mother NID", blank=True, default="")
    mother_dob = models.DateField(verbose_name="মাতার জন্ম তারিখ / Mother DOB", null=True, blank=True)
    mother_occupation = models.CharField(max_length=100, verbose_name="মাতার পেশা / Mother Occupation", blank=True, default="")

    guardian_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="অভিভাবকের নাম / Guardian Name")
    guardian_nid = models.CharField(max_length=50, blank=True, null=True, verbose_name="অভিভাবকের এনআইডি / Guardian NID")

    # Academic Info / শ্রেণী
    desired_class = models.CharField(max_length=50, verbose_name="শ্রেণী / Desired Class", default="Class 6")
    version = models.CharField(max_length=20, choices=[('Bangla', 'বাংলা ভার্সন'), ('English', 'English Version')], verbose_name="ভার্সন / Version", default="Bangla")

    # Present Address / বর্তমান ঠিকানা
    present_address_detail = models.TextField(verbose_name="বিস্তারিত ঠিকানা / Address Line", blank=True, default="")
    present_post_office = models.CharField(max_length=100, verbose_name="ডাকঘর / Post Office", blank=True, default="")
    present_division = models.CharField(max_length=100, verbose_name="বিভাগ / Division", blank=True, default="")
    present_district = models.CharField(max_length=100, verbose_name="জেলা / District", blank=True, default="")
    present_upazila = models.CharField(max_length=100, verbose_name="উপজেলা/থানা / Upazila", blank=True, default="")
    present_post_code = models.CharField(max_length=10, verbose_name="পোস্ট কোড / Post Code", blank=True, default="")

    # Permanent Address / স্থায়ী ঠিকানা
    permanent_address_detail = models.TextField(verbose_name="বিস্তারিত ঠিকানা / Address Line", blank=True, default="")
    permanent_post_office = models.CharField(max_length=100, verbose_name="ডাকঘর / Post Office", blank=True, default="")
    permanent_division = models.CharField(max_length=100, verbose_name="বিভাগ / Division", blank=True, default="")
    permanent_district = models.CharField(max_length=100, verbose_name="জেলা / District", blank=True, default="")
    permanent_upazila = models.CharField(max_length=100, verbose_name="উপজেলা/থানা / Upazila", blank=True, default="")
    permanent_post_code = models.CharField(max_length=10, verbose_name="পোস্ট কোড / Post Code", blank=True, default="")

    # Photo & Meta
    photo = models.ImageField(upload_to='student_photos/', verbose_name="ছবি / Photo", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Approved')
    
    # Backwards compatibility & tracking fields
    admission_no = models.CharField(max_length=50, blank=True, null=True)
    section = models.CharField(max_length=10, default="A", blank=True)
    roll_no = models.IntegerField(null=True, blank=True)
    academic_year = models.CharField(max_length=10, default="2026", blank=True)
    blood_group = models.CharField(max_length=10, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return self.student_name_bn or self.student_name_en or "Student"

    @name.setter
    def name(self, value):
        self.student_name_bn = value

    @property
    def student_class(self):
        return self.desired_class or "Class 6"

    @student_class.setter
    def student_class(self, value):
        self.desired_class = value

    @property
    def date_of_birth(self):
        return self.dob

    @date_of_birth.setter
    def date_of_birth(self, value):
        self.dob = value

    @property
    def guardian_phone(self):
        return self.mobile or ""

    @guardian_phone.setter
    def guardian_phone(self, value):
        self.mobile = value

    @property
    def address(self):
        return self.present_address_detail or ""

    @address.setter
    def address(self, value):
        self.present_address_detail = value

    def __str__(self):
        name = self.student_name_bn or self.student_name_en or "Student"
        return f"{name} - {self.desired_class}"

