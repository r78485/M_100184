import qrcode
import barcode
from barcode.writer import ImageWriter
import io
import base64
from django.shortcuts import render, get_object_or_404
from .models import Student, InstitutionProfile, GradingScale

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
                reg_no = f"2026100{adm.roll_no if adm.roll_no else adm.id}"
                adm_id = adm.admission_no or f"ADM-2026-{adm.id:04d}"
                student, _ = Student.objects.get_or_create(
                    student_id=adm_id,
                    defaults={
                        'registration_no': reg_no,
                        'name': adm.student_name_en or adm.student_name_bn or "Student",
                        'student_class': adm.desired_class or "Class 9",
                        'section': adm.section or "A",
                        'dob': adm.dob.strftime('%d-%m-%Y') if getattr(adm, 'dob', None) else "01-01-2010"
                    }
                )
    
    if student:
        results = student.results.all()
    else:
        # Dummy data for preview
        class DummyStudent:
            student_id = "0"
            registration_no = "2026100101"
            name = "Demo Student"
            student_class = "Class 9"
            section = "Science"
            dob = "01-01-2010"
        student = DummyStudent()
        results = []

    institution = InstitutionProfile.objects.first()
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

    # ২. অফলাইন QR Code জেনারেশন (Verification URL)
    qr = qrcode.QRCode(version=1, box_size=4, border=1)
    verify_url = f"https://{request.get_host()}/verify/transcript/{student.registration_no}/"
    qr.add_data(verify_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0d3b66", back_color="transparent")
    
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_code_b64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')

    # ৩. অফলাইন Barcode জেনারেশন (Registration/Serial No)
    EAN = barcode.get_barcode_class('code128')
    barcode_obj = EAN(student.registration_no, writer=ImageWriter())
    
    bc_buffer = io.BytesIO()
    barcode_obj.write(bc_buffer, options={"write_text": False, "quiet_zone": 2})
    barcode_b64 = base64.b64encode(bc_buffer.getvalue()).decode('utf-8')

    context = {
        'student': student,
        'institution': institution,
        'grading_scales': grading_scales,
        'results': processed_results,
        'cgpa': f"{cgpa:.2f}",
        'qr_code': qr_code_b64,
        'barcode': barcode_b64,
    }
    
    return render(request, 'transcript_template.html', context)
