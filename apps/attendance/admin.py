from django.contrib import admin
from .models import StudentAttendance, TeacherAttendance

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('date', 'status')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__roll_number')

@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'date', 'status')
    list_filter = ('date', 'status')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'teacher__username')
