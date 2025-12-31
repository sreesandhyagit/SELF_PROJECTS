from django.contrib import admin
from .models import Course,Teacher,Batch,Student,Enrollment

# Register your models here.

#Course Admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=('course_name','duration','fee')
    search_field=('course_name')

#Teacher Admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display=('teacher_name','teacher_email','teacher_phone','teacher_image')
    filter_horizontal=('courses',)

#Batch Admin
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_name', 'course', 'start_date')
    list_filter = ('course',)

#Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=('student_name','student_email','student_phone','platform')
    list_filter=('platform',)
    search_fields=('name',)

#Enrollment Admin
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display=('student','course','batch','joined_date')
    list_filter=('course','batch')
    
