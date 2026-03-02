from rest_framework import serializers
from .models import LessonProgress


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model=LessonProgress
        fields=[
            "id",
            "lesson",
            "is_completed",
            "watched_duration",
            "last_watched_at"
        ]
        read_only_fields=["last_watched_at"]