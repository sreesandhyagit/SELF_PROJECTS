from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Always allow these paths
        allowed_paths = [
            reverse('signin'),
            reverse('signup'),
        ]

        # Allow static & media
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # If not authenticated and not in allowed paths → redirect
        if not request.user.is_authenticated:
            if request.path not in allowed_paths:
                return redirect('signin')

        response = self.get_response(request)

        # Disable cache
        response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        return response
