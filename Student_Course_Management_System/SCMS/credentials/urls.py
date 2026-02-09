from django.urls import path
from . import views

# app_name = "credentials"

urlpatterns = [
    
    path("",views.signin,name="signin"),
    path("register/",views.register,name="signup"),   
    path("logout/",views.logout,name="logout")

]