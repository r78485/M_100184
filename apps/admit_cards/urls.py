from django.urls import path
from . import views

urlpatterns = [
    path('', views.admit_card_dashboard_view, name='admit_card_dashboard'),
    path('generate/', views.generate_admit_card, name='admit_cards_generate_all'),
    path('generate/student/<str:student_id>/', views.generate_admit_card, name='admit_cards_generate_student'),
]
