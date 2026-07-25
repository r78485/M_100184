from django.urls import path
from . import views

app_name = 'question_paper'

urlpatterns = [
    path('', views.create_paper_view, name='create'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit/<int:paper_id>/', views.create_paper_view, name='edit_paper'),
    path('subject-builder/<str:subject_code>/', views.subject_builder_view, name='subject_builder'),
    path('question-bank/', views.question_bank_view, name='question_bank'),
    path('history/', views.history_view, name='history'),
    path('print/<int:paper_id>/', views.print_preview_view, name='print_preview'),
    path('print-preview/', views.print_preview_view, name='print_preview_demo'),
    
    # API endpoints
    path('api/save-paper/', views.api_save_paper, name='api_save_paper'),
    path('api/create-mcq/', views.api_create_mcq, name='api_create_mcq'),
    path('api/bulk-create-mcq/', views.api_bulk_create_mcq, name='api_bulk_create_mcq'),
    path('api/ai-generate/', views.api_ai_generate, name='api_ai_generate'),
    path('api/delete-paper/<int:paper_id>/', views.api_delete_paper, name='api_delete_paper'),
]

