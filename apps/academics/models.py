from django.db import models
from django.conf import settings

class ClassRoom(models.Model):
    name = models.CharField(max_length=50) # e.g., Class 9
    section = models.CharField(max_length=10) # e.g., Section A

    def __str__(self):
        return f"{self.name} - {self.section}"

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, related_name='students')
    roll_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.get_full_name()} (Roll: {self.roll_number})"

# --- Question Builder Models ---

SUBJECT_CHOICES = [
    ('BANGLA', 'বাংলা'),
    ('ENGLISH', 'ইংরেজি'),
    ('MATH', 'গণিত'),
    ('SCIENCE', 'বিজ্ঞান'),
]

QUESTION_TYPE_CHOICES = [
    ('MCQ', 'বহুনির্বাচনী (MCQ)'),
    ('CREATIVE', 'সৃজনশীল / রচনামূলক'),
    ('SHORT', 'সংক্ষিপ্ত প্রশ্ন'),
    ('FILL_BLANK', 'শূন্যস্থান পূরণ'),
]

# ১. মূল প্রশ্ন মডেল (Base Question)
class QuestionBank(models.Model):
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    class_level = models.IntegerField(default=6)  # উদাহরণ: Class 6, 7, 8...
    marks = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - Class {self.class_level} ({self.question_type})"


# ২. বাংলা বিষয়ের জন্য বিশেষ ফিল্ড
class BanglaQuestion(models.Model):
    base_question = models.OneToOneField(QuestionBank, on_delete=models.CASCADE, related_name='bangla_detail')
    SECTION_CHOICES = [('PROSE', 'গদ্য'), ('POETRY', 'পদ্য'), ('GRAMMAR', 'ব্যাকরণ')]
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    passage = models.TextField(blank=True, null=True, help_text="উদ্দীপক / অনুচ্ছেদ")
    question_text = models.TextField(help_text="মূল প্রশ্ন")


# ৩. ইংরেজি বিষয়ের জন্য বিশেষ ফিল্ড
class EnglishQuestion(models.Model):
    base_question = models.OneToOneField(QuestionBank, on_delete=models.CASCADE, related_name='english_detail')
    SECTION_CHOICES = [('SEEN', 'Seen Passage'), ('UNSEEN', 'Unseen Passage'), ('GRAMMAR', 'Grammar'), ('WRITING', 'Writing')]
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    passage = models.TextField(blank=True, null=True, help_text="Comprehension Passage")
    question_text = models.TextField()


# ৪. গণিত বিষয়ের জন্য (LaTeX সমীকরণ সাপোর্ট সহ)
class MathQuestion(models.Model):
    base_question = models.OneToOneField(QuestionBank, on_delete=models.CASCADE, related_name='math_detail')
    CHAPTER_CHOICES = [('ALGEBRA', 'বীজগণিত'), ('GEOMETRY', 'জ্যামিতি'), ('ARITHMETIC', 'পাটিগণিত')]
    chapter_type = models.CharField(max_length=20, choices=CHAPTER_CHOICES)
    latex_formula = models.TextField(help_text="Math equations using LaTeX or standard text")
    has_diagram = models.BooleanField(default=False)
    diagram_image = models.ImageField(upload_to='math_diagrams/', blank=True, null=True)


# ৫. বিজ্ঞান বিষয়ের জন্য (চিত্র ও পর্যবেক্ষণ সাপোর্ট সহ)
class ScienceQuestion(models.Model):
    base_question = models.OneToOneField(QuestionBank, on_delete=models.CASCADE, related_name='science_detail')
    BRANCH_CHOICES = [('PHYSICS', 'পদার্থ'), ('CHEMISTRY', 'রসায়ন'), ('BIOLOGY', 'জীববিজ্ঞান'), ('GENERAL', 'সাধারণ')]
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
    stem_text = models.TextField(help_text="উদ্দীপক / পরীক্ষা বিবরণ")
    image = models.ImageField(upload_to='science_diagrams/', blank=True, null=True)
    question_text = models.TextField()
