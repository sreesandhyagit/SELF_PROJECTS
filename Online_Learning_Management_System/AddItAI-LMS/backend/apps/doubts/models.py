from django.db import models
from django.conf import settings
from apps.lessons.models import Lesson

# Create your models here.

User= settings.AUTH_USER_MODEL

class Doubt(models.Model):

    class Status(models.TextChoices):
        OPEN="OPEN"
        RESOLVED="RESOLVED"

    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name="doubts")
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name="asked_doubts")
    question=models.TextField()
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.OPEN)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.question[:40]}"
    
    
    
class Reply(models.Model):
    doubt=models.ForeignKey(Doubt,on_delete=models.CASCADE,related_name="replies")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    answer=models.TextField()
    upvotes=models.ManyToManyField(User,blank=True,related_name="upvoted_replies")
    created_at=models.DateTimeField(auto_now_add=True)

    def total_upvotes(self):
        return self.upvotes.count()
    


