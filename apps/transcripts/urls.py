from django.urls import path
from .views import generate_transcript, transcript_dashboard_view

urlpatterns = [
    path('', transcript_dashboard_view, name='transcript_dashboard'),
    path('transcript/<str:student_id>/', generate_transcript, name='generate_transcript'),
]
