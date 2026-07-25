from django.db import models
from django.conf import settings

SUBJECT_CHOICES = [
    ('BANGLA_1', 'বাংলা ১ম পত্র'),
    ('BANGLA_2', 'বাংলা ২য় পত্র'),
    ('ENGLISH_1', 'English First Paper'),
    ('ENGLISH_2', 'English Second Paper'),
    ('MATH', 'গণিত'),
    ('SCIENCE', 'সাধারণ বিজ্ঞান'),
    ('PHYSICS', 'পদার্থবিজ্ঞান'),
    ('CHEMISTRY', 'রসায়ন'),
    ('HIGHER_MATH', 'উচ্চতর গণিত'),
    ('ICT', 'তথ্য ও যোগাযোগ প্রযুক্তি (ICT)'),
]

QUESTION_TYPE_CHOICES = [
    ('CREATIVE', 'সৃজনশীল (CQ)'),
    ('MCQ', 'বহুনির্বাচনী (MCQ)'),
    ('SHORT', 'সংক্ষিপ্ত প্রশ্ন'),
    ('ESSAY', 'রচনামূলক প্রশ্ন'),
    ('PRACTICAL', 'ব্যবহারিক প্রশ্ন'),
    ('DIAGRAM', 'চিত্রভিত্তিক প্রশ্ন'),
    ('NUMERICAL', 'গাণিতিক সমস্যা'),
]

DIFFICULTY_CHOICES = [
    ('EASY', 'সহজ (Easy)'),
    ('MEDIUM', 'মধ্যম (Medium)'),
    ('HARD', 'কঠিন (Hard)'),
]

BOARD_CHOICES = [
    ('DHAKA', 'ঢাকা বোর্ড'),
    ('RAJSHAHI', 'রাজশাহী বোর্ড'),
    ('KHULNA', 'খুলনা বোর্ড'),
    ('BARISAL', 'বরিশাল বোর্ড'),
    ('SYLHET', 'সিলেট বোর্ড'),
    ('COMILLA', 'কুমিল্লা বোর্ড'),
    ('JESSORE', 'যশোর বোর্ড'),
    ('DINAJPUR', 'দিনাজপুর বোর্ড'),
    ('MYMENSINGH', 'ময়মনসিংহ বোর্ড'),
    ('CHITTAGONG', 'চট্টগ্রাম বোর্ড'),
    ('MADRASAH', 'মাদ্রাসা বোর্ড'),
    ('TECHNICAL', 'কারিগরি বোর্ড'),
]

CLASS_CHOICES = [
    ('Class 6', '৬ষ্ঠ শ্রেণি'),
    ('Class 7', '৭ম শ্রেণি'),
    ('Class 8', '৮ম শ্রেণি'),
    ('Class 9', '৯ম শ্রেণি'),
    ('Class 10', '১০ম শ্রেণি'),
    ('SSC', 'এসএসসি (SSC)'),
    ('Class 11', 'একাদশ শ্রেণি'),
    ('Class 12', 'দ্বাদশ শ্রেণি'),
    ('HSC', 'এইচএসসি (HSC)'),
]

class Chapter(models.Model):
    subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES)
    class_level = models.CharField(max_length=20, choices=CLASS_CHOICES, default='Class 9')
    chapter_number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=255, verbose_name="অধ্যায়ের নাম")
    description = models.TextField(blank=True, null=True, verbose_name="সংক্ষিপ্ত বিবরণ")
    topics_json = models.JSONField(default=list, blank=True, help_text="টপিক সমূহের তালিকা (List of topics)")
    progress = models.PositiveIntegerField(default=0, help_text="Completion percentage 0-100")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['class_level', 'subject', 'chapter_number']

    def __str__(self):
        return f"{self.get_class_level_display()} - {self.get_subject_display()} - অধ্যায় {self.chapter_number}: {self.title}"


class QuestionBank(models.Model):
    subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES)
    class_level = models.CharField(max_length=20, choices=CLASS_CHOICES, default='Class 9')
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    topic = models.CharField(max_length=250, blank=True, null=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='CREATIVE')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='MEDIUM')
    board_standard = models.CharField(max_length=20, choices=BOARD_CHOICES, blank=True, null=True)
    board_year = models.PositiveIntegerField(blank=True, null=True)
    marks = models.PositiveIntegerField(default=10)
    
    # Core Content
    question_text = models.TextField(verbose_name="মূল প্রশ্ন / নির্দেশনা", help_text="Supports MathJax, chemical formulas, HTML tables & code")
    answer_explanation = models.TextField(blank=True, null=True, verbose_name="উত্তর / সমাধান / ব্যাখ্যা")
    
    # Creative Question Builder (উদ্দীপক + ক/খ/গ/ঘ)
    stimulus_passage = models.TextField(blank=True, null=True, verbose_name="উদ্দীপক (Stimulus / Passage)")
    stimulus_image = models.ImageField(upload_to='question_stimulus/', blank=True, null=True)
    stimulus_table_data = models.JSONField(blank=True, null=True, help_text="Table or graph configuration")
    
    # Sub-questions for Creative Question
    q_ka = models.TextField(blank=True, null=True, verbose_name="ক নম্বর প্রশ্ন (1 Mark)")
    m_ka = models.PositiveIntegerField(default=1)
    q_kha = models.TextField(blank=True, null=True, verbose_name="খ নম্বর প্রশ্ন (2 Marks)")
    m_kha = models.PositiveIntegerField(default=2)
    q_ga = models.TextField(blank=True, null=True, verbose_name="গ নম্বর প্রশ্ন (3 Marks)")
    m_ga = models.PositiveIntegerField(default=3)
    q_gha = models.TextField(blank=True, null=True, verbose_name="ঘ নম্বর প্রশ্ন (4 Marks)")
    m_gha = models.PositiveIntegerField(default=4)
    
    # MCQ Fields
    option_a = models.CharField(max_length=500, blank=True, null=True, verbose_name="অপশন (ক)")
    option_b = models.CharField(max_length=500, blank=True, null=True, verbose_name="অপশন (খ)")
    option_c = models.CharField(max_length=500, blank=True, null=True, verbose_name="অপশন (গ)")
    option_d = models.CharField(max_length=500, blank=True, null=True, verbose_name="অপশন (ঘ)")
    correct_option = models.CharField(max_length=5, blank=True, null=True, choices=[('A','ক'),('B','খ'),('C','গ'),('D','ঘ')])
    negative_mark = models.FloatField(default=0.0)
    shuffle_options = models.BooleanField(default=True)

    # MCQ Extended Fields
    mcq_type = models.CharField(
        max_length=20, 
        choices=[('SINGLE', 'সাধারণ বহুনির্বাচনী'), ('POLYNOMIAL', 'বহুপদী সমাপ্তিসূচক'), ('PASSAGE', 'উদ্দীপকভিত্তিক')], 
        default='SINGLE'
    )
    statement_i = models.CharField(max_length=500, blank=True, null=True, verbose_name="বিবৃতি i")
    statement_ii = models.CharField(max_length=500, blank=True, null=True, verbose_name="বিবৃতি ii")
    statement_iii = models.CharField(max_length=500, blank=True, null=True, verbose_name="বিবৃতি iii")

    # Subject Special Data (MathJax/LaTeX/Chemistry/Physics/ICT code)
    latex_formula = models.TextField(blank=True, null=True, verbose_name="LaTeX / MathJax Formula")
    chemical_equation = models.TextField(blank=True, null=True, verbose_name="Chemical Formula / Equation")
    code_snippet = models.TextField(blank=True, null=True, verbose_name="Programming Code Snippet (ICT)")
    diagram_image = models.ImageField(upload_to='question_diagrams/', blank=True, null=True)

    # Meta
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_subject_display()}] Class {self.class_level} - {self.get_question_type_display()} ({self.marks}m)"


class QuestionPaperTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('BOARD', 'Board Style (NCTB Official)'),
        ('SCHOOL', 'School Standard Style'),
        ('MODERN', 'Modern Dynamic Style'),
        ('MADRASAH', 'Madrasah Board Style'),
        ('COLLEGE', 'College / Higher Secondary'),
        ('CUSTOM', 'Custom User Template'),
    ]
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES, default='BOARD')
    description = models.TextField(blank=True, null=True)
    style_config_json = models.JSONField(default=dict, blank=True, help_text="Font size, margins, grid columns settings")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"


class QuestionPaper(models.Model):
    NUMBERING_CHOICES = [
        ('BANGLA', 'Bangla (১, ২, ৩ / ক, খ, গ)'),
        ('ENGLISH', 'English (1, 2, 3 / a, b, c)'),
        ('ROMAN', 'Roman (i, ii, iii)'),
    ]

    FONT_CHOICES = [
        ('ARIAL', 'English - Arial / Inter'),
        ('TIMES', 'English - Times New Roman'),
        ('ROBOTO', 'English - Roboto'),
        ('KALPURUSH', 'Bangla - Kalpurush'),
        ('SOLAIMANLIPI', 'Bangla - SolaimanLipi'),
    ]

    COLUMN_CHOICES = [
        ('1', '1 Column (Full Width Standard)'),
        ('2', '2 Columns (NCTB Board Exam Style)'),
    ]
    
    PAPER_SIZE_CHOICES = [
        ('A4_PORTRAIT', 'A4 Portrait'),
        ('A4_LANDSCAPE', 'A4 Landscape'),
        ('LEGAL', 'Legal'),
        ('LETTER', 'Letter'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'খসড়া / Draft'),
        ('PUBLISHED', 'প্রকাশিত / Published'),
        ('ARCHIVED', 'আর্কাইভ / Archived'),
    ]

    # Header / Meta
    title = models.CharField(max_length=255, verbose_name="প্রশ্নপত্রের শিরোনাম / Exam Name", default="Annual Examination — 2026")
    academic_year = models.CharField(max_length=10, default="2026")
    class_name = models.CharField(max_length=50, default="Class 9")
    section = models.CharField(max_length=50, default="A", blank=True)
    subject = models.CharField(max_length=50, default="Mathematics")
    teacher_name = models.CharField(max_length=200, blank=True, null=True)
    exam_date = models.DateField(blank=True, null=True)
    time_allowed = models.CharField(max_length=100, default="3 Hours", verbose_name="পরীক্ষার সময়")
    
    # Marks Breakdown
    full_marks = models.PositiveIntegerField(default=100)
    pass_marks = models.PositiveIntegerField(default=33)
    written_marks = models.PositiveIntegerField(default=70)
    mcq_marks = models.PositiveIntegerField(default=30)
    creative_marks = models.PositiveIntegerField(default=70)
    
    # Header Details
    school_name = models.CharField(max_length=255, default="Gazimahmud Secondary School")
    school_logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    eiin_number = models.CharField(max_length=50, blank=True, null=True, default="EIIN: 123456")
    address = models.CharField(max_length=255, blank=True, null=True)

    # Styling & Layout Options
    font_family = models.CharField(max_length=30, choices=FONT_CHOICES, default='ARIAL')
    column_layout = models.CharField(max_length=5, choices=COLUMN_CHOICES, default='1')

    # Instructions
    instructions = models.TextField(
        default="1. Figures to the right indicate full marks.\n2. Read questions carefully before answering.\n3. Calculator is allowed where necessary."
    )
    
    # Footer Signatures & QR
    prepared_by = models.CharField(max_length=100, default="Subject Teacher")
    verified_by = models.CharField(max_length=100, default="Exam Controller")
    approved_by = models.CharField(max_length=100, default="Headmaster")
    show_qr_code = models.BooleanField(default=True)
    show_answer_key = models.BooleanField(default=False)
    
    # Questions & Formatting
    questions_json = models.JSONField(default=list, help_text="Ordered array of question objects, custom marks, numbers")
    numbering_style = models.CharField(max_length=20, choices=NUMBERING_CHOICES, default='ENGLISH')
    paper_size = models.CharField(max_length=20, choices=PAPER_SIZE_CHOICES, default='A4_PORTRAIT')
    margin_top_mm = models.PositiveIntegerField(default=15)
    margin_bottom_mm = models.PositiveIntegerField(default=15)
    margin_left_mm = models.PositiveIntegerField(default=15)
    margin_right_mm = models.PositiveIntegerField(default=15)
    
    # Security & Workflow
    template = models.ForeignKey(QuestionPaperTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    password_protection = models.CharField(max_length=128, blank=True, null=True)
    version = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.subject} ({self.class_name})"

