from django.shortcuts import render, redirect, get_object_or_404
from manager.models import Course, Teacher, Batch, Student, Enrollment
from .forms import CourseForm, TeacherForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
# from django.contrib import messages


# Create your views here.

def managerDashboard(request):
    return render(request,"manager-dashboard.html")

# Course -----------------------------------------------------------------------------------------------------------------

def courseList(request):
    courses = Course.objects.all()   
   
    search = request.GET.get("search")
    if search:
        courses = courses.filter(course_name=search)         

    form = CourseForm()

    for c in courses:        
        c.form=CourseForm(instance=c)               
   
    return render(request, 'course.html', {'courses': courses, 'form': form})

def addCourse(request):
    if request.method == 'POST':
        my_form = CourseForm(request.POST)
        if my_form.is_valid():
            my_form.save()
            return redirect('course_list')
        else:
            print(my_form.errors)
            return redirect("course_list")
    else:
        my_form=CourseForm()
    return redirect('course_list',{"form":my_form})

def editCourse(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        my_form = CourseForm(request.POST, instance=course)
        if my_form.is_valid():
            my_form.save()
            return redirect('course_list')
        else:
            print(my_form.errors)
            return redirect("course_list")
    else:
        my_form=CourseForm(instance=course)
    return render(request,'course.html',{'courses':Course.objects.all(),'form':my_form})

def deleteCourse(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        course.delete()
    return redirect('course_list')

# Teacher-------------------------------------------------------------------------------------------------------------

# def teachersList(request):
#     teachers = Teacher.objects.all()   
   
#     search = request.GET.get("search")
#     if search:
#         teachers = teachers.filter(teacher_name=search)         

#     form = TeacherForm()

#     for t in teachers:        
#         t.form=CourseForm(instance=t)               
   
#     return render(request, 'teacher.html', {'teachers': teachers, 'form': form})
    
class TeachersList(ListView):
    model = Teacher
    template_name = "teacher.html"
    context_object_name = "teachers"
    paginate_by = 3

    def get_queryset(self):
        return Teacher.objects.prefetch_related('courses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # for prefill data in form
        for teacher in context['teachers']:
            teacher.form = TeacherForm(instance=teacher)
        context['form'] = TeacherForm()  # for ADD modal
        return context
    
# def addTeacher(request):
#     if request.method == 'POST':
#         my_form = TeacherForm(request.POST,request.FILES)
#         if my_form.is_valid():
#             my_form.save()
#             return redirect('teacher_list')
#         else:
#             print(my_form.errors)
#             return redirect("teacher_list")
#     else:
#         my_form=TeacherForm()
#     return redirect('teacher.html',{"form":my_form})

class AddTeacher(CreateView):
    model = Teacher
    form_class = TeacherForm
    success_url = reverse_lazy('teacher_list')

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

# def editTeacher(request, id):
#     teacher = get_object_or_404(Teacher, id=id)
#     if request.method == 'POST':
#         my_form = TeacherForm(request.POST,request.FILES, instance=teacher)
#         if my_form.is_valid():
#             my_form.save()
#             return redirect('teacher_list')
#         else:
#             print(my_form.errors)
#             return redirect("teacher_list")
#     else:
#         my_form=TeacherForm(instance=teacher)
#     # return render(request,'teacher.html',{'teachers':teacher,'form':my_form})
#     return render(request,'teacher.html',{'teachers':Teacher.objects.all(),'form':my_form})

class EditTeacher(UpdateView):
    model = Teacher
    form_class = TeacherForm
    success_url = reverse_lazy('teacher_list')

# def deleteTeacher(request, id):
#     course = get_object_or_404(Course, id=id)
#     if request.method == 'POST':
#         course.delete()
#     return redirect('course_list')

class DeleteTeacher(DeleteView):
    model = Teacher
    success_url = reverse_lazy('teacher_list')

#Batch----------------------------------------------------------------------------------------------------------------

def batch(request):
    return render(request,"batch.html")

def student(request):
    return render(request,"student.html")

def enrollment(request):
    return render(request,"enrollment.html")

