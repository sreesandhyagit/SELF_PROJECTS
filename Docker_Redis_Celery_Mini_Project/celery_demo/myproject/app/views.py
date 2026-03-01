from django.http import HttpResponse,JsonResponse
from .tasks import test_task, send_welcome_email

# Create your views here.

def run_task(request):
    test_task.delay()
    return HttpResponse("Task Triggered!")

def run_email_task(request):
    task = send_welcome_email.delay("Sreesandhya")
    return JsonResponse({
        "message":"Task started!",
        "task_id":task.id
        })

