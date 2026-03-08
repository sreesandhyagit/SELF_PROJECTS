from django.db import models
from django.db import models
from django.conf import settings
from apps.orders.models import Order

User = settings.AUTH_USER_MODEL

# Create your models here.

class Payment(models.Model):
    PAYMENT_STATUS=[
        ("pending","Pending"),
        ("success","Success"),
        ("failed","Failed")
    ]
    PAYMENT_METHODS=[
        ("razorpay","Razorpay"),
        ("stripe","Stripe"),
        ("manual","Manual")
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="payments")
    order=models.OneToOneField(Order,on_delete=models.CASCADE,related_name="payment")
    payment_id=models.CharField(max_length=255,blank=True,null=True)
    method=models.CharField(max_length=20,choices=PAYMENT_METHODS,default="razorpay")
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,choices=PAYMENT_STATUS,default="pending")
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes=[
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"
    