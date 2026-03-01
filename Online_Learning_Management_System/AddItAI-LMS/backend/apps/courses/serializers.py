from rest_framework import serializers
from .models import Course
from apps.lessons.serializers import SectionWithLessonsSerializer


class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.ReadOnlyField(source="instructor.username")
    is_free = serializers.ReadOnlyField()
    sections=SectionWithLessonsSerializer(many=True,read_only=True)
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["id","slug","instructor","created_at","updated_at"]

