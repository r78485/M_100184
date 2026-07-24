from django.shortcuts import render, get_object_or_404
from .models import Student, SchoolProfile

from apps.users.models import StudentAdmission

def admit_card_dashboard_view(request):
    class_name = request.GET.get('class_name', '')
    
    admissions = StudentAdmission.objects.all().order_by('-created_at')
    
    if class_name:
        admissions = admissions.filter(desired_class__icontains=class_name)
        
    db_classes = StudentAdmission.objects.values_list('desired_class', flat=True).distinct()
    db_classes = [c for c in db_classes if c]
    
    standard_classes = ['Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10', 'SSC 2024', 'SSC 2025', 'SSC 2026']
    classes = list(set(standard_classes + db_classes))
    classes.sort()
    
    context = {
        'students': admissions,
        'classes': classes,
        'selected_class': class_name,
    }
    return render(request, 'admit_card_dashboard.html', context)

from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def generate_admit_card(request, student_id=None):
    school = SchoolProfile.objects.first() # অথবা সক্রিয় প্রোফাইল
    
    class DummySubject:
        def __init__(self, code, name):
            self.code = code
            self.name = name

    class SubjectManager:
        def all(self):
            return [DummySubject("101", "Bangla"), DummySubject("107", "English"), DummySubject("109", "Mathematics")]

    class MappedStudent:
        def __init__(self, adm):
            self.student_id = adm.admission_no
            self.serial_no = f"100{adm.roll_no}" if adm.roll_no else "1000"
            self.name = adm.student_name_en or adm.student_name_bn
            self.father_name = adm.father_name
            self.mother_name = adm.mother_name
            self.roll_no = str(adm.roll_no) if adm.roll_no else "N/A"
            self.reg_no = f"2026100{adm.roll_no}" if adm.roll_no else "N/A"
            self.student_class = adm.student_class
            self.session = adm.academic_year
            self.group = adm.section if adm.section else "General"
            self.examinee_type = "REGULAR"
            self.subjects = SubjectManager()

    students = []
    
    if student_id:
        if student_id != '0':
            adm = StudentAdmission.objects.filter(admission_no=student_id).first()
            if adm:
                students = [MappedStudent(adm)]
    else:
        # নির্দিষ্ট শ্রেণীর সব ছাত্রের জন্য (Bulk Print)
        class_name = request.GET.get('class_name')
        if class_name:
            admissions = StudentAdmission.objects.filter(desired_class=class_name)
            students = [MappedStudent(adm) for adm in admissions]

    if not students:
        # Create a dummy student for preview if database is empty or not found
        class DummyStudent:
            def __init__(self, sid, name, cls, roll):
                self.student_id = sid
                self.serial_no = f"100{roll}"
                self.name = name
                self.father_name = "Mr. Dummy Father"
                self.mother_name = "Mrs. Dummy Mother"
                self.roll_no = roll
                self.reg_no = f"2026100{roll}"
                self.student_class = cls
                self.session = "2026-2027"
                self.group = "Science"
                self.examinee_type = "REGULAR"
                self.subjects = SubjectManager()

        cls_name = request.GET.get('class_name', "Class 9")
        target_id = student_id if student_id else "S-501"
        
        students = [
            DummyStudent(target_id, "Arif Rahman (Demo)", cls_name, "101"),
            DummyStudent("S-502", "Jannatul Ferdous (Demo)", cls_name, "102"),
            DummyStudent("S-503", "Rakib Hasan (Demo)", cls_name, "103")
        ]
        
    if not school:
        class DummyImage:
            @property
            def url(self):
                return "/static/logo.png"

        class DummySchool:
            name_en = "EduManage International School"
            name_bn = "এডুম্যানেজ ইন্টারন্যাশনাল স্কুল"
            address = "Barguna Sadar, Barguna - 8700"
            eiin = "100184"
            logo = DummyImage()
            controller_signature = None
        school = DummySchool()

    context = {
        'school': school,
        'students': students,
    }
    return render(request, 'admit_card_template.html', context)
