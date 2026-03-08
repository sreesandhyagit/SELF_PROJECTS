from django.db import models
from django.conf import settings
from apps.courses.models import Course

User=settings.AUTH_USER_MODEL

# Create your models here.

class Review(models.Model):

    RATING_CHOICES=[
        (1,"1 Stars"),
        (2,"2 Stars"),
        (3,"3 Stars"),
        (4,"4 Stars"),
        (5,"5 Stars"),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="reviews")
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="reviews")
    rating=models.IntegerField(choices=RATING_CHOICES)
    comment=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=["user","course"]
        ordering=["-created_at"]
    
    def __str__(self):
        return f"{self.user} - {self.course} - {self.rating}"
    
    