import uuid
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Student, InstitutionProfile
from datetime import date
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from apps.users.models import StudentAdmission

from django.contrib.auth.decorators import login_required

# Dashboard / Search View for Testimonial
@login_required
def testimonial_dashboard_view(request):

    class_name = request.GET.get('class_name', '')
    roll_no = request.GET.get('roll_no', '')
    
    # Ensure some dummy data exists for testing if DB is empty
    if StudentAdmission.objects.count() == 0:
        import datetime
        StudentAdmission.objects.create(
            admission_no="ADM-2026-001",
            student_name_en="Hasibul Islam",
            student_class="Class 9",
            section="Science",
            roll_no=120,
            academic_year="2026",
            date_of_birth=datetime.date(2010, 5, 15),
            father_name="Md. Rafiqul Islam",
            mother_name="Hasina Begum",
            guardian_phone="01711000000",
            address="Ghaibandha Sadar"
        )
        StudentAdmission.objects.create(
            admission_no="ADM-2026-002",
            student_name_en="Nusrat Jahan",
            student_class="Class 9",
            section="Arts",
            roll_no=121,
            academic_year="2026",
            date_of_birth=datetime.date(2011, 2, 20),
            father_name="Md. Abdur Rahman",
            mother_name="Farida Yasmin",
            guardian_phone="01722000000",
            address="Ghaibandha Sadar"
        )
        
    # Search in the central student database
    admissions = StudentAdmission.objects.all().order_by('-created_at')
    
    if class_name:
        admissions = admissions.filter(desired_class__icontains=class_name)
    if roll_no:
        try:
            admissions = admissions.filter(roll_no=int(roll_no))
        except ValueError:
            pass
            
    db_classes = StudentAdmission.objects.values_list('desired_class', flat=True).distinct()
    db_classes = [c for c in db_classes if c]
    
    standard_classes = ['Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10', 'SSC 2024', 'SSC 2025', 'SSC 2026']
    classes = list(set(standard_classes + db_classes))
    classes.sort()
    
    # Map to context structure expected by template
    students_list = []
    for adm in admissions:
        # Check if testimonial already generated
        test_student = Student.objects.filter(sl_no=adm.admission_no).first()
        
        students_list.append({
            'sl_no': adm.admission_no,
            'token_number': test_student.token_number if test_student else 'TKN-PENDING',
            'name': adm.student_name_en or adm.student_name_bn,
            'father_name': adm.father_name,
            'student_class': adm.student_class,
            'exam_year': adm.academic_year,
            'gpa': test_student.gpa if test_student else 'N/A',
            'is_testimonial_printed': test_student.is_testimonial_printed if test_student else False
        })
    
    context = {
        'students': students_list,
        'classes': classes,
        'selected_class': class_name,
        'search_roll': roll_no,
    }
    return render(request, 'testimonial_dashboard.html', context)

from django.views.decorators.clickjacking import xframe_options_exempt

# HTML View with Token
@xframe_options_exempt
def testimonial_view(request, student_id=None):
    active_school_name = request.session.get('school_name', 'গাজীমাহমুদ নিম্ন মাধ্যমিক বিদ্যালয়')
    
    institution = InstitutionProfile.objects.first()
    
    if not institution:
        class DummyInstitution:
            name_en = "Gazi Mahmud Secondary School"
            name_bn = active_school_name
            address_bn = "গাইবান্ধা সদর, জেলা: গাইবান্ধা"
            established_year = "২০১৪"
            logo = None
        institution = DummyInstitution()
    elif "স্নিগ্ধ" in institution.name_bn:
        institution.name_bn = active_school_name
        institution.name_en = "Gazi Mahmud Secondary School"
        institution.save()

    if student_id:
        student = Student.objects.filter(sl_no=student_id).first()
        if not student and student_id != '0':
            adm = StudentAdmission.objects.filter(admission_no=student_id).first()
            if adm:
                village_val = getattr(adm, 'present_address_detail', '') or getattr(adm, 'permanent_address_detail', '') or "গাইবান্ধা সদর"
                district_val = getattr(adm, 'present_district', '') or getattr(adm, 'permanent_district', '') or "গাইবান্ধা"
                upazila_val = getattr(adm, 'present_upazila', '') or getattr(adm, 'permanent_upazila', '') or "গাইবান্ধা সদর"
                
                dob_val = "01-01-2010"
                raw_dob = getattr(adm, 'dob', None) or getattr(adm, 'date_of_birth', None)
                if raw_dob:
                    if hasattr(raw_dob, 'strftime'):
                        dob_val = raw_dob.strftime('%d-%m-%Y')
                    else:
                        dob_val = str(raw_dob)

                student = Student.objects.create(
                    sl_no=adm.admission_no or student_id,
                    student_class=getattr(adm, 'student_class', '') or getattr(adm, 'desired_class', 'Class 9'),
                    roll_no=str(getattr(adm, 'roll_no', '')) if getattr(adm, 'roll_no', None) else "",
                    name=getattr(adm, 'student_name_en', '') or getattr(adm, 'student_name_bn', '') or "Student",
                    father_name=getattr(adm, 'father_name', '') or "Father Name",
                    mother_name=getattr(adm, 'mother_name', '') or "Mother Name",
                    village=village_val,
                    post_office="গাইবান্ধা",
                    upazila=upazila_val,
                    district=district_val,
                    exam_year=getattr(adm, 'academic_year', '2026') or "2026",
                    gpa="5.00",
                    dob=dob_val
                )

    else:
        student = None
        
    if not student:
        # Dummy data for preview
        class DummyStudent:
            sl_no = "ADM-2026-002"
            token_number = "TKN-2026-6CFCF9"
            name = "Nusrat Jahan"
            father_name = "Md. Abdur Rahman"
            mother_name = "Farida Yasmin"
            village = "Gaibandha Sadar"
            post_office = "Gaibandha"
            upazila = "Gaibandha Sadar"
            district = "Gaibandha"
            exam_year = "2026"
            gpa = "5.00"
            dob = "20-02-2011"
            issue_date = date.today()
        student = DummyStudent()

    # Format exam year cleanly so "২০2026" is prevented
    raw_year = str(getattr(student, 'exam_year', '2026'))
    clean_exam_year = raw_year if len(raw_year) == 4 else f"20{raw_year}"

    context = {
        'student': student,
        'institution': institution,
        'clean_exam_year': clean_exam_year,
    }
    return render(request, 'testimonial_template.html', context)


# PDF View using ReportLab
def generate_pdf_with_token(request, student_id):
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors
        from reportlab.pdfgen import canvas
        from reportlab.graphics.barcode import code128
    except ImportError:
        return HttpResponse("ReportLab is not installed. Please run: pip install reportlab", status=500)
        
    student = get_object_or_404(Student, sl_no=student_id)
    institution = InstitutionProfile.objects.first()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="certificate_{student.token_number}.pdf"'
    
    page_width, page_height = landscape(A4)
    c = canvas.Canvas(response, pagesize=landscape(A4))

    stub_width = 180 # বামপাশের টোকেন অংশের সাইজ

    # ==========================================
    # ১. বামপাশের টোকেন / স্টাব সেকশন
    # ==========================================
    c.saveState()
    c.setFillColor(colors.HexColor("#F8F9FA"))
    c.rect(0, 0, stub_width, page_height, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#1A7A3E"))
    c.rect(0, page_height - 50, stub_width, 50, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(stub_width / 2, page_height - 30, "OFFICE TOKEN STUB")

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    y = page_height - 80
    c.drawString(12, y, f"Token: {student.token_number}")
    c.setFont("Helvetica", 8)
    c.drawString(12, y - 18, f"Student ID: {student.sl_no}")
    c.drawString(12, y - 32, f"Name: {student.name}")
    c.drawString(12, y - 46, f"Issue Date: {student.issue_date.strftime('%d/%m/%Y')}")

    # বারকোড জেনারেটর (টোকেন পার্টের জন্য)
    token_barcode = code128.Code128(student.token_number, barHeight=28, barWidth=0.9)
    token_barcode.drawOn(c, 12, y - 90)

    # কাটা লাইন (Dashed Cut Line)
    c.setStrokeColor(colors.HexColor("#888888"))
    c.setLineWidth(1)
    c.setDash(4, 4)
    c.line(stub_width, 0, stub_width, page_height)
    c.restoreState()

    # ==========================================
    # ২. মূল প্রশংসা পত্র সেকশন (ডানপাশে)
    # ==========================================
    cert_start_x = stub_width
    cert_width = page_width - stub_width

    # সিকিউরিটি বর্ডার
    c.saveState()
    margin = 15
    ox, oy = cert_start_x + margin, margin
    w, h = cert_width - (2 * margin), page_height - (2 * margin)
    
    c.setStrokeColor(colors.HexColor("#1A7A3E"))
    c.setLineWidth(2)
    c.rect(ox, oy, w, h, fill=0, stroke=1)
    c.restoreState()

    # ওয়াটারমার্ক
    c.saveState()
    c.setFillColor(colors.HexColor("#F0F7F2"))
    c.setFont("Helvetica-Bold", 22)
    c.translate(cert_start_x + (cert_width / 2), page_height / 2)
    c.rotate(30)
    inst_en = institution.name_en if institution else "SNIGDHA GYANER ALO VIDYAPITH"
    c.drawCentredString(0, 0, inst_en)
    c.restoreState()

    # মূল প্রশংসাপত্রের টপ-রাইটে রেফারেন্স বারকোড
    cert_barcode = code128.Code128(student.token_number, barHeight=18, barWidth=0.8)
    cert_barcode.drawOn(c, page_width - 140, page_height - 65)

    # হেডার ও বিবরণী
    center_x = cert_start_x + (cert_width / 2)
    c.setFillColor(colors.HexColor("#B81414"))
    c.setFont("Helvetica-Bold", 18)
    inst_bn = institution.name_bn if institution else "স্নিগ্ধ জ্ঞানের আলো বিদ্যাপীঠ"
    
    # ReportLab doesn't support Bengali Unicode well out of the box without custom fonts.
    # We will draw it, but it might show as boxes unless a font is registered. 
    # Usually, a custom TTF must be registered for Bengali text.
    c.drawCentredString(center_x, page_height - 60, "PROSHONGSHA POTRO") # Fallback since BN might crash or show boxes

    # PDF পেজ সমাপ্তি
    c.showPage()
    c.save()

    return response

@csrf_exempt
def mark_testimonial_printed(request, student_id):
    if request.method == 'POST':
        student = Student.objects.filter(sl_no=student_id).first()
        if student:
            student.is_testimonial_printed = True
            student.testimonial_printed_at = timezone.now()
            student.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Student not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
