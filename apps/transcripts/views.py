import datetime
import qrcode
import barcode
from barcode.writer import ImageWriter
import io
import base64
from django.shortcuts import render, get_object_or_404
from .models import Student, StudentResult, InstitutionProfile, GradingScale

from apps.users.models import StudentAdmission
from django.db.models import Q
from django.views.decorators.clickjacking import xframe_options_exempt

def transcript_dashboard_view(request):
    try:
        from school_management.middleware import auto_repair_student_admission_schema
        auto_repair_student_admission_schema()
    except Exception:
        pass

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
    return render(request, 'transcript_dashboard.html', context)

@xframe_options_exempt
def generate_transcript(request, student_id):
    student = None
    results = []

    if student_id and student_id != "0":
        student = Student.objects.filter(Q(student_id=student_id) | Q(registration_no=student_id)).first()
        if not student:
            try:
                from school_management.middleware import auto_repair_student_admission_schema
                auto_repair_student_admission_schema()
            except Exception:
                pass
            adm = StudentAdmission.objects.filter(Q(admission_no=student_id) | Q(id=student_id if student_id.isdigit() else 0)).first()
            if adm:
                roll = getattr(adm, 'roll_no', None) or adm.id
                reg_no = f"2026100{roll}"
                adm_id = adm.admission_no or f"ADM-2026-{adm.id:04d}"
                
                dob_val = getattr(adm, 'dob', None)
                if not dob_val or not isinstance(dob_val, datetime.date):
                    dob_val = datetime.date(2010, 1, 1)

                student, _ = Student.objects.get_or_create(
                    student_id=adm_id,
                    defaults={
                        'roll_no': str(roll),
                        'registration_no': reg_no,
                        'session': getattr(adm, 'academic_year', None) or "2025-2026",
                        'full_name': adm.student_name_en or adm.student_name_bn or "Student",
                        'father_name': getattr(adm, 'father_name', '') or "Father Name",
                        'mother_name': getattr(adm, 'mother_name', '') or "Mother Name",
                        'exam_name': "J.S.C / S.S.C Examination",
                        'group_or_subject': adm.desired_class or "Science",
                        'dob': dob_val
                    }
                )

    if student:
        if not student.results.exists():
            sample_results = [
                ('101', 'Bangla First Paper', 100, 82),
                ('102', 'Bangla Second Paper', 100, 78),
                ('107', 'English First Paper', 100, 85),
                ('108', 'English Second Paper', 100, 80),
                ('109', 'Mathematics', 100, 92),
                ('111', 'Physics', 100, 88),
                ('112', 'Chemistry', 100, 84),
                ('113', 'Higher Mathematics', 100, 90),
                ('150', 'Bangladesh & Global Studies', 100, 78),
                ('154', 'Information & Communication Technology', 50, 46),
            ]
            for code, sname, total_m, obt_m in sample_results:
                StudentResult.objects.create(
                    student=student,
                    subject_code=code,
                    subject_name=sname,
                    total_credit_or_marks=total_m,
                    obtained_marks=obt_m
                )
        results = student.results.all()
    else:
        # Dummy data for preview
        class DummyStudent:
            student_id = "0"
            roll_no = "01"
            registration_no = "2026100101"
            session = "2025-2026"
            full_name = "Demo Student"
            father_name = "Demo Father"
            mother_name = "Demo Mother"
            exam_name = "J.S.C / S.S.C Examination"
            group_or_subject = "Science"
            dob = datetime.date(2010, 1, 1)
        student = DummyStudent()
        results = []

    from apps.admit_cards.models import SchoolProfile
    sp = SchoolProfile.objects.first()
    institution = InstitutionProfile.objects.first()
    if not institution:
        institution = InstitutionProfile.objects.create(
            name_en=sp.name_en if (sp and sp.name_en) else "Gazimahmud Junior High School",
            name_bn=sp.name_bn if (sp and sp.name_bn) else "গাজীমাহমুদ নিম্ন মাধ্যমিক বিদ্যালয়",
            eiin=sp.eiin if (sp and sp.eiin) else "100184",
            board_or_authority="Directorate of Secondary and Higher Education"
        )
    elif sp:
        if sp.name_en: institution.name_en = sp.name_en
        if sp.name_bn: institution.name_bn = sp.name_bn
        if sp.eiin: institution.eiin = sp.eiin
        if sp.logo: institution.logo = sp.logo
        if sp.seal: institution.seal = sp.seal
        if sp.controller_signature: institution.controller_signature = sp.controller_signature

    if not GradingScale.objects.exists():
        scales = [
            (80, 100, 'A+', 5.00, 'Outstanding'),
            (70, 79, 'A', 4.00, 'Excellent'),
            (60, 69, 'A-', 3.50, 'Very Good'),
            (50, 59, 'B', 3.00, 'Good'),
            (40, 49, 'C', 2.00, 'Satisfactory'),
            (33, 39, 'D', 1.00, 'Pass'),
            (0, 32, 'F', 0.00, 'Fail'),
        ]
        for m_from, m_to, l_grade, g_point, rem in scales:
            GradingScale.objects.create(
                mark_from=m_from,
                mark_to=m_to,
                letter_grade=l_grade,
                grade_point=g_point,
                remarks=rem
            )

    grading_scales = GradingScale.objects.all()

    # ১. পয়েন্ট ও জিপিএ (GPA) হিসাব
    total_points = 0
    total_subjects = 0 if not results else results.count()
    has_failed = False

    processed_results = []
    for res in results:
        l_grade, g_point = res.get_grade_info()
        if g_point == 0:
            has_failed = True
        total_points += g_point
        processed_results.append({
            'code': res.subject_code,
            'name': res.subject_name,
            'marks': res.obtained_marks,
            'grade': l_grade,
            'point': f"{g_point:.2f}"
        })

    cgpa = 0.00 if has_failed or total_subjects == 0 else (total_points / total_subjects)

    # ২. অফলাইন QR Code জেনারেশন (Accurate Academic Transcript View URL)
    from django.urls import reverse
    target_id = getattr(student, 'student_id', None) or student_id
    try:
        rel_path = reverse('generate_transcript', args=[target_id])
        verify_url = request.build_absolute_uri(rel_path)
    except Exception:
        verify_url = f"{request.scheme}://{request.get_host()}/transcripts/transcript/{target_id}/"

    qr = qrcode.QRCode(version=1, box_size=4, border=1)
    qr.add_data(verify_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0d3b66", back_color="white")
    
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_code_b64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')

    # ৩. অফলাইন Barcode জেনারেশন (Student ID)
    raw_barcode_val = str(getattr(student, 'student_id', None) or student_id)
    clean_barcode = "".join(c for c in raw_barcode_val if c.isalnum() or c in "-_")
    if not clean_barcode:
        clean_barcode = "STD100184"

    EAN = barcode.get_barcode_class('code128')
    barcode_obj = EAN(clean_barcode, writer=ImageWriter())
    
    bc_buffer = io.BytesIO()
    barcode_obj.write(bc_buffer, options={"write_text": False, "quiet_zone": 2})
    barcode_b64 = base64.b64encode(bc_buffer.getvalue()).decode('utf-8')

    context = {
        'student': student,
        'institution': institution,
        'school_profile': sp,
        'grading_scales': grading_scales,
        'results': processed_results,
        'cgpa': f"{cgpa:.2f}",
        'qr_code': qr_code_b64,
        'barcode': barcode_b64,
        'verify_url': verify_url,
    }
    
    return render(request, 'transcript_template.html', context)

