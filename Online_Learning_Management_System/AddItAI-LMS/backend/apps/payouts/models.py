from django.db import models
from apps.accounts.models import User

# Create your models here.

class Payout(models.Model):

    STATUS_CHOICES=[
        ("PENDING","Pending"),
        ("APPROVED","Approved"),
        ("PAID","Paid"),
        ("REJECTED","Rejected")
    ]
    instructor=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="PENDING")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.instructor} - {self.amount}"
    
