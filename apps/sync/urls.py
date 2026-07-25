from django.urls import path
from . import views

urlpatterns = [
    # অনলাইন সার্ভার থেকে ডেটা রিসিভ করা (লোকাল → অনলাইন push এর গন্তব্য)
    path('push/', views.sync_receive_push, name='sync_push'),

    # অনলাইন সার্ভার থেকে ডেটা এক্সপোর্ট (লোকাল এখানে GET করে)
    path('export/', views.sync_export_data, name='sync_export'),

    # AJAX স্ট্যাটাস চেক
    path('status/', views.sync_status_api, name='sync_status'),

    # ম্যানুয়াল সিঙ্ক ট্রিগার
    path('trigger/', views.trigger_manual_sync, name='sync_trigger'),
]
