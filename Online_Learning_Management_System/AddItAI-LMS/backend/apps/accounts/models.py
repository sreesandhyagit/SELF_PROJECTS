from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

# identity

class User(AbstractUser):

    class Role(models.TextChoices):  # TextChoices is Cleaner and safer than tuple choices.
        ADMIN = "ADMIN", "Admin"
        INSTRUCTOR = "INSTRUCTOR", "Instructor"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(max_length = 20,choices = Role.choices, default=Role.STUDENT)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", blank = True, null = True)
    is_email_verified = models.BooleanField(default=False) # Authentication purpose
    is_instructor_approved = models.BooleanField(default=False) # Approval for role pupose

    def __str__(self):
        return f"{self.username}({self.get_role_display()})"   
    

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
    
class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="instructor_profile")

    qualification = models.CharField(max_length=255)
    experience = models.TextField()
    skills = models.TextField()

    demo_video = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null = True)
    portfolio = models.URLField(blank=True,null=True)

    rating = models.FloatField(default=0)
    total_students = models.IntegerField(default=0)
    total_courses = models.IntegerField(default=0)

    bio = models.TextField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)
    
    @property
    def level(self):
        if self.rating < 2:
            return "Beginner"
        elif self.rating < 4:
            return "Intermediate"
        else:
            return "Expert"
        



class InstructorRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='instructor_requests')
    status = models.CharField(max_length=20, choices = Status.choices, default=Status.PENDING)
    reason = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_requests')

    def save(self, *args, **kwargs):
        if self.status == self.Status.APPROVED:
            if not self.user.is_instructor:
                self.user.role = User.Role.INSTRUCTOR
                self.user.is_instructor_approved = True
                self.user.save()
                # InstructorProfile.objects.get_or_create(user=self.user) # create profile code, but not need bcz signals.py created
        super().save(*args,**kwargs)


        
        
    

   
    


