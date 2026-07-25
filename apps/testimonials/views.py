import uuid
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Student, InstitutionProfile
from datetime import date
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from apps.users.models import StudentAdmission

from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Dashboard / Search View for Testimonial
@login_required
def testimonial_dashboard_view(request):
    class_name = request.GET.get('class_name', '').strip()
    roll_no = request.GET.get('roll_no', '').strip()
    
    # Query central Student Registry
    admissions = StudentAdmission.objects.all().order_by('-created_at')
    
    if class_name:
        admissions = admissions.filter(
            Q(desired_class__icontains=class_name) | Q(desired_class__endswith=class_name)
        )
        
    if roll_no:
        admissions = admissions.filter(
            Q(student_name_en__icontains=roll_no) | 
            Q(student_name_bn__icontains=roll_no) | 
            Q(father_name__icontains=roll_no) | 
            Q(admission_no__icontains=roll_no) |
            Q(roll_no__icontains=roll_no)
        )

    db_classes = list(StudentAdmission.objects.values_list('desired_class', flat=True).distinct())
    db_classes += list(Student.objects.values_list('student_class', flat=True).distinct())
    db_classes = [c for c in db_classes if c]
    
    standard_classes = ['Class 6', 'Class 7', 'Class 8', 'Class 9', 'Class 10', 'SSC 2024', 'SSC 2025', 'SSC 2026']
    classes = list(set(standard_classes + db_classes))
    classes.sort()
    
    students_list = []
    seen_ids = set()
    
    for adm in admissions:
        adm_id = adm.admission_no or f"ADM-2026-{adm.id:04d}"
        seen_ids.add(adm_id)
        test_student = Student.objects.filter(sl_no=adm_id).first()
        
        students_list.append({
            'sl_no': adm_id,
            'token_number': test_student.token_number if test_student else 'TKN-PENDING',
            'name': adm.student_name_en or adm.student_name_bn or "Student",
            'father_name': adm.father_name or "",
            'student_class': adm.desired_class or "Class 9",
            'exam_year': adm.academic_year or "2026",
            'gpa': test_student.gpa if test_student else '5.00',
            'is_testimonial_printed': test_student.is_testimonial_printed if test_student else False
        })
        
    # Also include standalone records from Student table
    t_students = Student.objects.all()
    if class_name:
        t_students = t_students.filter(student_class__icontains=class_name)
    if roll_no:
        t_students = t_students.filter(
            Q(roll_no__icontains=roll_no) | Q(name__icontains=roll_no) | Q(sl_no__icontains=roll_no)
        )
        
    for ts in t_students:
        if ts.sl_no not in seen_ids:
            seen_ids.add(ts.sl_no)
            students_list.append({
                'sl_no': ts.sl_no,
                'token_number': ts.token_number,
                'name': ts.name,
                'father_name': ts.father_name,
                'student_class': ts.student_class or "Class 9",
                'exam_year': ts.exam_year or "2026",
                'gpa': ts.gpa or "5.00",
                'is_testimonial_printed': ts.is_testimonial_printed
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
    active_school_address = request.session.get('school_address', 'গাইবান্ধা সদর, জেলা: গাইবান্ধা')
    
    try:
        from apps.admit_cards.models import SchoolProfile
        sp = SchoolProfile.objects.first()
        if sp:
            if sp.name_bn or sp.name_en:
                active_school_name = sp.name_bn or sp.name_en
            if sp.address:
                active_school_address = sp.address
    except Exception:
        pass
    
    institution = InstitutionProfile.objects.first()
    
    if not institution:
        class DummyInstitution:
            name_en = "Gazi Mahmud Secondary School"
            name_bn = active_school_name
            address_bn = active_school_address
            established_year = "২০১৪"
            logo = None
        institution = DummyInstitution()
    else:
        institution.name_bn = active_school_name
        institution.address_bn = active_school_address
        institution.save()

    if student_id:
        student = Student.objects.filter(sl_no=student_id).first()
        if not student and student_id != '0':
            adm = StudentAdmission.objects.filter(Q(admission_no=student_id) | Q(id=student_id if student_id.isdigit() else 0)).first()
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
        'school_name': active_school_name,
        'school_address': active_school_address,
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
