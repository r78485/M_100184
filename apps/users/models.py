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

# Model Aliases for backward compatibility
Student = StudentAdmission


class Employee(models.Model):
    emp_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100, blank=True, default="Staff")
    dept = models.CharField(max_length=100, blank=True, default="General")
    email = models.CharField(max_length=150, blank=True, default="")
    join_date = models.CharField(max_length=50, blank=True, default="")
    active = models.BooleanField(default=True)
    username = models.CharField(max_length=100, blank=True, default="")
    pass_val = models.CharField(max_length=100, blank=True, default="12345")
    father_name = models.CharField(max_length=200, blank=True, default="")
    mother_name = models.CharField(max_length=200, blank=True, default="")
    spouse_name = models.CharField(max_length=200, blank=True, default="")
    dob = models.CharField(max_length=50, blank=True, default="")
    gender = models.CharField(max_length=20, blank=True, default="Male")
    blood = models.CharField(max_length=10, blank=True, default="A+")
    religion = models.CharField(max_length=50, blank=True, default="Islam")
    nid = models.CharField(max_length=50, blank=True, default="")
    index_no = models.CharField(max_length=50, blank=True, default="")
    appointment_date = models.CharField(max_length=50, blank=True, default="")
    first_mpo = models.CharField(max_length=50, blank=True, default="")
    pay_code = models.CharField(max_length=20, blank=True, default="20")
    primary_phone = models.CharField(max_length=30, blank=True, default="")
    present_addr = models.TextField(blank=True, default="")
    edu = models.CharField(max_length=200, blank=True, default="")
    exp = models.CharField(max_length=100, blank=True, default="")
    basic_salary = models.CharField(max_length=50, blank=True, default="12,000")
    photo = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        default_photo = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%230284c7'><path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z'/></svg>"
        return {
            'id': self.emp_id,
            'idCode': self.emp_id,
            'serialNo': self.emp_id,
            'registrationId': self.emp_id,
            'indexNo': self.index_no or self.emp_id,
            'nid': self.nid or self.emp_id,
            'nationalId': self.nid or self.emp_id,
            'name': self.name,
            'name_en': self.name,
            'role': self.role,
            'desigEn': self.role,
            'dept': self.dept,
            'email': self.email,
            'emailAddress': self.email,
            'joinDate': self.join_date,
            'dateOfJoining': self.join_date,
            'active': self.active,
            'username': self.username,
            'pass': self.pass_val,
            'fatherName': self.father_name,
            'fatherOrHusbandName': self.father_name,
            'motherName': self.mother_name,
            'spouseName': self.spouse_name,
            'dob': self.dob,
            'dateOfBirth': self.dob,
            'gender': self.gender,
            'blood': self.blood,
            'bloodGroup': self.blood,
            'religion': self.religion,
            'appointmentDate': self.appointment_date,
            'firstMPO': self.first_mpo,
            'firstMpoDate': self.first_mpo,
            'payCode': self.pay_code,
            'primaryPhone': self.primary_phone,
            'mobileNo': self.primary_phone,
            'presentAddr': self.present_addr,
            'homeAddress': self.present_addr,
            'edu': self.edu,
            'education': self.edu,
            'exp': self.exp,
            'experience': self.exp,
            'basicSalary': self.basic_salary,
            'monthlySalary': self.basic_salary,
            'status': 'Active' if self.active else 'Inactive',
            'photo': self.photo or default_photo
        }

    def __str__(self):
        return f"{self.name} ({self.role})"


