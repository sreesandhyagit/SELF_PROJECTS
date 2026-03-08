from django.db import models
from django.conf import settings
from apps.courses.models import Course

# Create your models here.

User = settings.AUTH_USER_MODEL

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart_items")
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="cart_courses")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user","course"]
        ordering = ["-added_at"]
        indexes = [
            models.Index(fields=["user"])
        ]

    def __str__(self):
        return f"{self.user} - {self.course.title}"