from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from django.contrib import messages
from credentials.models import Profile
from django.db import transaction


# # Create your views here.
# def register(request):
#     if request.method == "POST":
#         first_name = request.POST.get("f_name")
#         last_name = request.POST.get("l_name")
#         pro_pic = request.FILES.get("profile_picture")
#         mail = request.POST.get("email")
#         role = request.POST.get("role")
#         password = request.POST.get("password")

#         if not role:
#             messages.error(request, "Please select a role")
#             return redirect("signup")

#         if User.objects.filter(username=mail).exists():
#             messages.error(request, "User already exists")
#             return redirect("signup")

#         try:
#             with transaction.atomic():
#                 user = User.objects.create_user(
#                     username=mail,
#                     first_name=first_name,
#                     last_name=last_name,
#                     email=mail,
#                     password=password
#                 )

#                 profile, created = Profile.objects.get_or_create(user=user)
#                 profile.profile_pic = pro_pic
#                 profile.role = role     
#                 profile.save()

#                 messages.success(request, "Registration successful")
#                 return redirect("signin")

#         except Exception as e:
#             messages.error(request, f"Can't create new user: {e}")
#             return redirect("signup")

#     return render(request, "register.html")


# def signin(request):
#     if request.user.is_authenticated:
#         return redirect("dashboard")

#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]

#         user = auth.authenticate(request, username=username, password=password)

#         if user is not None:
#             auth.login(request, user)
#             return redirect("dashboard")  
#         else:
#             messages.error(request, "Invalid username or password")

#     return render(request, "login.html")



# REGISTER --------------------------------------------------------------------
def register(request):

    if request.user.is_authenticated:
        return redirect("dashboard")  # redirect logged-in users
    
    if request.method == "POST":
        first_name = request.POST.get("f_name")
        last_name = request.POST.get("l_name")
        pro_pic = request.FILES.get("profile_picture")
        mail = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validate passwords
        if password != confirm_password:
            messages.error(request, "Password mismatch!")
            return redirect("signup")

        # Check if user already exists
        if User.objects.filter(username=mail).exists():
            messages.error(request, "User already exists")
            return redirect("signup")

        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(
                    username=mail,
                    first_name=first_name,
                    last_name=last_name,
                    email=mail,
                    password=password
                )

                # Profile is auto-created by signals
                # profile, created = Profile.objects.get_or_create(user=user)
                profile=user.profile
                profile.profile_pic = pro_pic
                profile.role = "staff"  # default role for new users
                profile.save()

                messages.success(request, "Registration successful! Please login.")
                return redirect("signin")

        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect("signup")

    return render(request, "register.html")

# LOGIN ----------------------------------------------------------------------
def signin(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # Role-based redirect
            profile = user.profile
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "login.html")

# LOGOUT -----------------------------------------
def logout(request):
    auth.logout(request)
    return redirect("signin")
