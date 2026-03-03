from django.db import models
from apps.lessons.models import Lesson
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.

class LessonProgress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE)
    is_completed=models.BooleanField(default=False)
    watched_duration=models.PositiveIntegerField(default=0) # seconds
    last_watched_at=models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=["user","lesson"]
        indexes=[models.Index(fields=["user","last_watched_at"]),]

    def __str__(self):
        return f"{self.user} - {self.lesson}"