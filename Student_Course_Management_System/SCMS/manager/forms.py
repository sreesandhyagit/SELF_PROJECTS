from django import forms
from .models import Course,Teacher

class CourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields="__all__"
        exclude=["slug"]
        widgets={
            "course_name":forms.TextInput(attrs={"class":"form-control"}),
            "duration":forms.TextInput(attrs={"class":"form-control"}),
            "fee":forms.NumberInput(attrs={"class":"form-control"})
        }
        
class TeacherForm(forms.ModelForm):
    class Meta:
        model=Teacher
        fields="__all__"
        exclude=["slug"]
        widgets={
            "teacher_image":forms.ClearableFileInput(attrs={"class":"form-control"}),
            "teacher_name":forms.TextInput(attrs={"class":"form-control"}),
            "teacher_phone":forms.TextInput(attrs={"class":"form-control"}),
            "teacher_email":forms.EmailInput(attrs={"class":"form-control"}),
            "courses":forms.CheckboxSelectMultiple()
        }
        