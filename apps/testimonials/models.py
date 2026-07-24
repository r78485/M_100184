import uuid
from django.db import models

class InstitutionProfile(models.Model):
    name_bn = models.CharField(max_length=255, default="স্নিগ্ধ জ্ঞানের আলো বিদ্যাপীঠ")
    name_en = models.CharField(max_length=255, default="SNIGDHA GYANER ALO VIDYAPITH")
    address_bn = models.CharField(max_length=255, default="গাইবান্ধা সদর, জেলা: গাইবান্ধা")
    established_year = models.CharField(max_length=20, default="২০১৪ইং")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    
    def __str__(self):
        return self.name_bn

class Student(models.Model):
    sl_no = models.CharField(max_length=50)
    student_class = models.CharField(max_length=50, blank=True, null=True, verbose_name="শ্রেণী")
    roll_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="রোল নম্বর")
    token_number = models.CharField(max_length=50, unique=True, editable=False) # টোকেন নম্বর
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    post_office = models.CharField(max_length=100)
    upazila = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    exam_year = models.CharField(max_length=10)
    gpa = models.CharField(max_length=10)
    dob = models.CharField(max_length=20)
    issue_date = models.DateField(auto_now_add=True)
    is_testimonial_printed = models.BooleanField(default=False)
    testimonial_printed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token_number:
            # অটোমেটিক ইউনিক টোকেন নম্বর জেনারেট (যেমন: TKN-2026-8891)
            self.token_number = f"TKN-2026-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.token_number})"
