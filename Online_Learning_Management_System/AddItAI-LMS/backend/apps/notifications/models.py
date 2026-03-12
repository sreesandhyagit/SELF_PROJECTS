from django.db import models
from django.conf import settings

User= settings.AUTH_USER_MODEL

# Create your models here.

class Notification(models.Model):
    
    NOTIFICATION_TYPES=[
        ("ENROLLMENT","Enrollment"),
        ("PAYMENT","Payment"),
        ("CERTIFICATE","Certificate"),
        ("QNA","Question & Answer"),
        ("SYSTEM","System"),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="notifications")
    title=models.CharField(max_length=255)
    message=models.TextField()
    notification_type=models.CharField(max_length=20,choices=NOTIFICATION_TYPES,default="SYSTEM")
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["-created_at"]
        indexes=[models.Index(fields=["user","is_read"]),]

    def __str__(self):
        return f"{self.user} - {self.title}"


