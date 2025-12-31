from django.urls import path
from manager import views

urlpatterns = [
    path("",views.managerDashboard,name="dashboard"),

    path("courses",views.courseList,name="course_list"),
    path('courses/add', views.addCourse, name='add_course'),
    path('courses/edit/<int:id>/', views.editCourse, name='edit_course'),
    path('courses/delete/<int:id>/', views.deleteCourse, name='delete_course'),

    path("teachers",views.TeachersList.as_view(),name="teacher_list"),
    path('teachers/add', views.AddTeacher.as_view(), name='add_teacher'),
    path('teachers/edit/<int:pk>/', views.EditTeacher.as_view(), name='edit_teacher'),
    path('teachers/delete/<int:pk>/', views.DeleteTeacher.as_view(), name='delete_teacher'),

    path("batch",views.batch,name="batch"),

    path("student",views.student,name="student"),
    
    path("enrollment",views.enrollment,name="enrollment"),   
    
    

  
]
