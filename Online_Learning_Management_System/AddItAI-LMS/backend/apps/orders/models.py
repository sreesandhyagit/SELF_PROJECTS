from django.db import models
from django.conf import settings
from apps.courses.models import Course


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES=[
        ("PENDING","Pending"),
        ("PAID","Paid"),        
        ("FAILED","Failed"),
        ("CANCELLED","Cancelled")
    ]
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    course=models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    amount=models.DecimalField(max_digits=8,decimal_places=2)

    status=models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    payment_id=models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["-created_at"]        
        indexes=[
            models.Index(fields=["user","status"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.course} - {self.status}"
    

