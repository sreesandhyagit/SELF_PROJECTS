from django.db.models.signals import post_save
from django.dispatch import receiver
from credentials.models import Profile
from django.contrib.auth.models import User

# (Optional) Auto-create Profile when User is created 
# This avoids errors like User has no profile.

# Auto-create Profile for each new User
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



