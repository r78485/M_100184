from django.contrib import admin
from django.urls import path, include
from apps.users import views as user_views
from apps.academics import views as academics_views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import ensure_icons

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

def favicon_view(request):
    svg_icon = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="#0284c7"/><path d="M50 20 L80 40 L50 60 L20 40 Z" fill="#ffffff"/><path d="M35 53 L35 70 C35 75 65 75 65 70 L65 53" fill="none" stroke="#ffffff" stroke-width="5"/></svg>'
    return HttpResponse(svg_icon, content_type="image/svg+xml")

urlpatterns = [
    path('favicon.ico', favicon_view),
    path('static/icon-192x192.png', favicon_view),
    path('admin/', admin.site.urls),
    path('', user_views.dashboard_router, name='dashboard'),
    path('login/', user_views.admin_login_view, name='login'),
    path('logout/', user_views.custom_logout, name='logout'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('transcripts/', include('apps.transcripts.urls')),
    path('admit-card/', include('apps.admit_cards.urls')),
    path('testimonial/', include('apps.testimonials.urls')),
    
    # PWA Support
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type='application/javascript'), name='sw.js'),
    path('manifest.json', TemplateView.as_view(template_name="manifest.json", content_type='application/json'), name='manifest.json'),
    
    # Dashboards (Role-Restricted in views.py)
    path('dashboard/admin/', user_views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/teacher/', user_views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', user_views.student_dashboard, name='student_dashboard'),
    
    # Settings (Role-Restricted in views.py)
    path('settings/general/', user_views.general_settings, name='general_settings'),
    path('settings/account/', user_views.account_settings, name='account_settings'),
    
    # Public Pages
    path('online-admission/', TemplateView.as_view(template_name='online_admission.html'), name='online_admission'),
    path('admission-slip/<int:admission_id>/', user_views.admission_slip_view, name='admission_slip'),
    path('api/save-student/', user_views.api_save_student, name='api_save_student'),
    path('api/students/', user_views.api_get_students, name='api_get_students'),
    path('api/approve-student/<int:student_id>/', user_views.api_approve_student, name='api_approve_student'),
    path('api/delete-student/<int:student_id>/', user_views.api_delete_student, name='api_delete_student'),
    path('backup/cloud/', user_views.trigger_cloud_backup, name='trigger_backup'),
    path('backup/download-full/', user_views.download_full_backup, name='download_full_backup'),
    path('backup/database/', user_views.backup_database_view, name='backup_database'),
    path('clone/student-admission/<int:pk>/', user_views.clone_student_admission, name='clone_student_admission'),

    # Administration
    path('admin-panel/admissions/', login_required(TemplateView.as_view(template_name='admissions.html')), name='admissions'),
    path('admin-panel/classes/', login_required(TemplateView.as_view(template_name='classes.html')), name='classes'),
    path('admin-panel/subjects/', login_required(TemplateView.as_view(template_name='subjects.html')), name='subjects'),
    path('admin-panel/students/', login_required(TemplateView.as_view(template_name='students.html')), name='students'),
    path('admin-panel/employees/', login_required(TemplateView.as_view(template_name='employees.html')), name='employees'),
    
    # Finance
    path('finance/accounts/', login_required(TemplateView.as_view(template_name='accounts.html')), name='accounts'),
    path('finance/fees/', login_required(TemplateView.as_view(template_name='fees.html')), name='fees'),
    path('finance/salary/', login_required(TemplateView.as_view(template_name='salary.html')), name='salary'),
    path('finance/store/', login_required(TemplateView.as_view(template_name='store.html')), name='store'),
    
    # Daily Operations
    path('operations/attendance/', login_required(TemplateView.as_view(template_name='attendance.html')), name='attendance'),
    path('operations/timetable/', login_required(TemplateView.as_view(template_name='timetable.html')), name='timetable'),
    path('operations/homework/', login_required(TemplateView.as_view(template_name='homework.html')), name='homework'),
    path('operations/behaviour/', login_required(TemplateView.as_view(template_name='behaviour.html')), name='behaviour'),
    
    # Communication
    path('communication/whatsapp/', login_required(TemplateView.as_view(template_name='whatsapp.html')), name='whatsapp'),
    path('communication/messaging/', login_required(TemplateView.as_view(template_name='messaging.html')), name='messaging'),
    path('communication/sms/', login_required(TemplateView.as_view(template_name='sms.html')), name='sms'),
    path('communication/liveclass/', login_required(TemplateView.as_view(template_name='liveclass.html')), name='liveclass'),
    
    # Assessments
    path('assessments/exams/', login_required(TemplateView.as_view(template_name='exams.html')), name='exams'),
    path('assessments/classtests/', login_required(TemplateView.as_view(template_name='classtests.html')), name='classtests'),
    path('assessments/questionpaper/', login_required(TemplateView.as_view(template_name='questionpaper.html')), name='questionpaper'),
    path('assessments/certificates/', login_required(TemplateView.as_view(template_name='certificates.html')), name='certificates'),
    path('assessments/reports/', login_required(TemplateView.as_view(template_name='reports.html')), name='reports'),
    path('result-card/', user_views.generate_result_card, name='result_card'),
    
    # Registration Card & Course Certificate Dashboards
    path('registration-card/', user_views.registration_card_dashboard_view, name='registration_card_dashboard'),
    path('registration-card/generate/<str:student_id>/', user_views.generate_registration_card, name='generate_registration_card'),
    path('course-certificate/', user_views.course_certificate_dashboard_view, name='course_certificate_dashboard'),
    path('course-certificate/generate/<str:student_id>/', user_views.generate_course_certificate, name='generate_course_certificate'),
    
    # Question Builder (Academics)
    path('question/create/<str:subject_name>/', academics_views.create_subject_question, name='create_subject_question'),
    path('question/success/<int:question_id>/', academics_views.question_success, name='question_success'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

