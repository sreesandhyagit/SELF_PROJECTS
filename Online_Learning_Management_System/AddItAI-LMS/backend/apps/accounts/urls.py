from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, ToggleUserActiveView
from .views import InstructorProfileView, CreateInstructorRequestView, InstructorRequestListView, ReviewInstructorRequestView


urlpatterns = [

    path('register/', RegisterView.as_view()),
    path('login/',LoginView.as_view()),

    path("profile/",UserProfileView.as_view()),
    
    path('toggle-user/<int:user_id>/', ToggleUserActiveView.as_view()),

    path('instructor/profile/',InstructorProfileView.as_view()),
    path('request-instructor/', CreateInstructorRequestView.as_view()),
    path('instructor-requests/', InstructorRequestListView.as_view()),
    path('review-request/<int:pk>/', ReviewInstructorRequestView.as_view())

]
