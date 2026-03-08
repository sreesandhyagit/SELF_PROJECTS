from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    course_title=serializers.CharField(source="course.title",read_only=True)

    class Meta:
        model=Order
        fields=[
            "id",
            "course",
            "course_title",
            "amount",
            "status",
            "payment_id",
            "created_at"
        ]
        read_only_fields=["status","payment_id"]
        