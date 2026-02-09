from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    ROLE_CHOICES=(
        ("admin","Admin"),
        ("teacher","Teacher"),
        ("staff","Staff")
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic=models.ImageField(upload_to="profile/",default="credentials/images/default_profile_image.png")
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default="staff")

    def __str__(self):
        return f"{self.user.username} ({self.role})"