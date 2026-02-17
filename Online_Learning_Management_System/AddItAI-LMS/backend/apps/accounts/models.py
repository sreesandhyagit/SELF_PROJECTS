from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# identity

class User(AbstractUser):

    class Role(models.TextChoices):  # TextChoices is Cleaner and safer than tuple choices.
        ADMIN = "ADMIN", "Admin"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(
        max_length = 20,
        choices = Role.choices,
        default=Role.STUDENT
    )

    bio = models.TextField(blank=True, null=True)

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank = True,
        null = True
    )

    is_email_verified = models.BooleanField(default=False) # Authentication purpose

    is_instructor_approved = models.BooleanField(default=False) # Approval for role pupose

    def __str__(self):
        return f"{self.username}({self.role})"
    

    # helper properties for role checking

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_instructor(self):
        return self.role == self.Role.INSTRUCTOR

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT
    
    
    
   
    


