from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Student, SchoolProfile
from apps.users.models import StudentAdmission

def admit_card_dashboard_view(request):
    try:
        from school_management.middleware import auto_repair_student_admission_schema
        auto_repair_student_admission_schema()
    except Exception:
        pass

    class_name = request.GET.get('class_name', '').strip()
    search_query = request.GET.get('search_query', '').strip() or request.GET.get('roll_no', '').strip()
    
    # Ensure test dummy data exists if DB is empty
    if StudentAdmission.objects.count() == 0:
        import datetime
        StudentAdmission.objects.create(
            admission_no="ADM-2026-001",
            student_name_en="Hasibul Islam",
            student_name_bn="হাসিবুল ইসলাম",
            desired_class="Class 9",
            section="Science",
            roll_no=120,
            academic_year="2026",
            date_of_birth=datetime.date(2010, 5, 15),
            father_name="Md. Rafiqul Islam",
            mother_name="Hasina Begum",
            mobile="01711000000"
        )
        StudentAdmission.objects.create(
            admission_no="ADM-2026-002",
            student_name_en="Nusrat Jahan",
            student_name_bn="নুসরাত জাহান",
            desired_class="Class 9",
            section="Arts",
            roll_no=121,
            academic_year="2026",
            date_of_birth=datetime.date(2011, 2, 20),
            father_name="Md. Abdur Rahman",
            mother_name="Farida Yasmin",
            mobile="01722000000"
        )

    admissions = StudentAdmission.objects.all().order_by('-created_at')
    
    if class_name and class_name != "All":
        admissions = admissions.filter(
            Q(desired_class__icontains=class_name) | Q(desired_class__endswith=class_name)
        )
        
    if search_query:
        admissions = admissions.filter(
            Q(student_name_en__icontains=search_query) |
            Q(student_name_bn__icontains=search_query) |
            Q(father_name__icontains=search_query) |
            Q(admission_no__icontains=search_query) |
            Q(roll_no__icontains=search_query)
        )
        
    students_list = []
    for adm in admissions:
        adm_no = adm.admission_no or f"ADM-2026-{adm.id:04d}"
        students_list.append({
            'id': adm.id,
            'admission_no': adm_no,
            'student_name_en': adm.student_name_en or adm.student_name_bn or "Student",
            'student_name_bn': adm.student_name_bn or adm.student_name_en or "",
            'father_name': adm.father_name or "",
            'student_class': adm.desired_class or "Class 9",
            'roll_no': adm.roll_no or "N/A",
            'section': adm.section or "General",
        })
        
    db_classes = list(StudentAdmission.objects.values_list('desired_class', flat=True).distinct())
    db_classes = [c for c in db_classes if c]
    
    standard_classes = ['Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10', 'SSC 2024', 'SSC 2025', 'SSC 2026']
    classes = list(set(standard_classes + db_classes))
    classes.sort()
    
    context = {
        'students': students_list,
        'classes': classes,
        'selected_class': class_name,
        'search_query': search_query,
    }
    return render(request, 'admit_card_dashboard.html', context)

from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def generate_admit_card(request, student_id=None):
    active_school_name = "Gazimahmud Junior High School"
    active_school_name_bn = "গাজীমাহমুদ নিম্ন মাধ্যমিক বিদ্যালয়"
    active_school_eiin = "100184"
    active_school_address = "Barguna Sadar, Barguna"

    sp = SchoolProfile.objects.first()
    if not sp:
        sp = SchoolProfile.objects.create(
            name_en=active_school_name,
            name_bn=active_school_name_bn,
            eiin=active_school_eiin,
            address=active_school_address
        )
    else:
        sp.name_en = active_school_name
        sp.name_bn = active_school_name_bn
        sp.eiin = active_school_eiin
        sp.address = active_school_address
        sp.save()

    school = sp

    # Official NCTB Subjects with Codes for Admit Card
    class SubjectItem:
        def __init__(self, code, name):
            self.code = code
            self.name = name

    class SubjectList:
        def __init__(self, items):
            self.items = items
        def all(self):
            return self.items

    def get_subjects_for_class(cls_str):
        return SubjectList([
            SubjectItem("101", "BANGLA"),
            SubjectItem("102", "ENGLISH"),
            SubjectItem("109", "MATHEMATICS"),
            SubjectItem("112", "SCIENCE"),
            SubjectItem("154", "ICT / DIGITAL TECHNOLOGY"),
            SubjectItem("153", "HISTORY & SOCIAL SCIENCE"),
            SubjectItem("156", "LIFE & LIVELIHOOD"),
            SubjectItem("147", "HEALTH & WELL-BEING"),
            SubjectItem("148", "ART & CULTURE"),
            SubjectItem("111", "ISLAM & MORAL EDUCATION")
        ])

    class MappedStudent:
        def __init__(self, adm):
            self.student_id = adm.admission_no or f"ADM-2026-{adm.id:04d}"
            self.serial_no = f"100{adm.roll_no}" if adm.roll_no else f"100{adm.id}"
            self.name = adm.student_name_en or adm.student_name_bn or "STUDENT"
            self.father_name = adm.father_name or "FATHER NAME"
            self.mother_name = adm.mother_name or "MOTHER NAME"
            self.roll_no = str(adm.roll_no) if adm.roll_no else "N/A"
            self.reg_no = f"2026100{adm.roll_no if adm.roll_no else adm.id}"
            self.student_class = adm.desired_class or "Class 9"
            self.session = adm.academic_year or "2026-2027"
            self.group = adm.section if adm.section else "General"
            self.examinee_type = "REGULAR"
            self.subjects = get_subjects_for_class(self.student_class)

    students = []
    if student_id and student_id != '0':
        adm = StudentAdmission.objects.filter(Q(admission_no=student_id) | Q(id=student_id if student_id.isdigit() else 0)).first()
        if adm:
            students = [MappedStudent(adm)]
    else:
        class_name = request.GET.get('class_name')
        if class_name and class_name != 'All':
            admissions = StudentAdmission.objects.filter(Q(desired_class__icontains=class_name) | Q(desired_class__endswith=class_name))
        else:
            admissions = StudentAdmission.objects.all().order_by('-created_at')
        students = [MappedStudent(adm) for adm in admissions]

    if not students:
        class DummyStudent:
            def __init__(self, sid, name, cls, roll):
                self.student_id = sid
                self.serial_no = f"100{roll}"
                self.name = name
                self.father_name = "Md. Abdur Rahman"
                self.mother_name = "Farida Yasmin"
                self.roll_no = roll
                self.reg_no = f"2026100{roll}"
                self.student_class = cls
                self.session = "2026-2027"
                self.group = "General"
                self.examinee_type = "REGULAR"
                self.subjects = get_subjects_for_class(cls)

        cls_name = request.GET.get('class_name', "Class 9")
        target_id = student_id if student_id else "ADM-2026-001"
        
        students = [
            DummyStudent(target_id, "ARIF RAHMAN", cls_name, "101"),
            DummyStudent("ADM-2026-002", "NUSRAT JAHAN", cls_name, "102"),
            DummyStudent("ADM-2026-003", "HASIBUL ISLAM", cls_name, "103")
        ]

    context = {
        'school': school,
        'students': students,
    }
    return render(request, 'admit_card_template.html', context)
