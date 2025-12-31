from django.db.models.signals import pre_save,post_save,pre_delete,post_delete
from django.dispatch import receiver
from manager.models import Teacher
import media

# from django.http import HttpResponse
# from django.core.exceptions import PermissionDenied
# import os

