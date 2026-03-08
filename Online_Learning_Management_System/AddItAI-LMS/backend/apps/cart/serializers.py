from rest_framework import serializers
from .models import Cart
from apps.courses.models import Course


class CartSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(
        source="course.title",
        read_only=True
    )
    course_price = serializers.DecimalField(
        source="course.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    class Meta:
        model = Cart
        fields = [
            "id",
            "course",
            "course_title",
            "course_price",
            "added_at"
        ]