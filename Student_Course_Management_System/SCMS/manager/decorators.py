from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("signin")

        if request.user.is_superuser or request.user.profile.role == "admin":
            return view_func(request, *args, **kwargs)

        raise PermissionDenied

    return wrapper
