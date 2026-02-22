from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, InstructorProfile

@receiver(post_save,sender=User)
def create_instructor_profile(sender,instance,**kwargs):
    if instance.role == User.Role.INSTRUCTOR and instance.is_instructor_approved:
        InstructorProfile.objects.get_or_create(user=instance)

        