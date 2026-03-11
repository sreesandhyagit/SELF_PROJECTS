from django.db import models
from django.conf import settings
from apps.courses.models import Course
import uuid

User=settings.AUTH_USER_MODEL

# Create your models here.

class Certificate(models.Model):
    certificate_id=models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="certificates")
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="certificates")
    issued_at=models.DateTimeField(auto_now_add=True)
    certificate_file=models.FileField(upload_to="certificates/",blank=True,null=True)

    class Meta:
        unique_together=["user","course"]

    def __str__(self):
        return f"{self.user} - {self.course}"
    
