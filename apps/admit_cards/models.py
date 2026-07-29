from django.db import models

class SchoolProfile(models.Model):
    name_bn = models.CharField(max_length=255, verbose_name="প্রতিষ্ঠানের নাম (বাংলা)")
    name_en = models.CharField(max_length=255, verbose_name="প্রতিষ্ঠানের নাম (ইংরেজি)")
    eiin = models.CharField(max_length=50)
    address = models.CharField(max_length=255, verbose_name="ঠিকানা", blank=True, null=True)
    logo = models.ImageField(upload_to='logos/')
    seal = models.ImageField(upload_to='seals/', null=True, blank=True, verbose_name="প্রতিষ্ঠানের সিল (Round Seal)")
    controller_signature = models.ImageField(upload_to='signatures/', null=True, blank=True)

    def __str__(self):
        return self.name_bn

class Subject(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    serial_no = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    mother_name = models.CharField(max_length=150)
    roll_no = models.CharField(max_length=50)
    reg_no = models.CharField(max_length=50)
    student_class = models.CharField(max_length=50, verbose_name="শ্রেণী")
    session = models.CharField(max_length=50)
    group = models.CharField(max_length=50)
    examinee_type = models.CharField(max_length=50, default="REGULAR")
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return f"{self.name} ({self.roll_no})"
