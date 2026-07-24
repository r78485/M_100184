from django.urls import path
from . import views

urlpatterns = [
    path('', views.testimonial_dashboard_view, name='testimonial_dashboard'),
    path('generate/student/<str:student_id>/', views.testimonial_view, name='testimonial_generate'),
    path('generate/pdf/<str:student_id>/', views.generate_pdf_with_token, name='testimonial_generate_pdf'),
    path('mark-printed/<str:student_id>/', views.mark_testimonial_printed, name='mark_testimonial_printed'),
]
