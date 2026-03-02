from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class Enrollment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="enrollments")
    course=models.ForeignKey("courses.Course",on_delete=models.CASCADE,related_name="enrollments")
    is_active=models.BooleanField(default=True)
    enrolled_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=["user","course"]
    
    def __str__(self):
        return f"{self.user} -> {self.course}"
    
