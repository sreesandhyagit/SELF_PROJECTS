from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    course_title=serializers.CharField(source="course.title",read_only=True)

    class Meta:
        model=Certificate
        fields=[
            "certificate_id",
            "course",
            "course_title",
            "issued_at",
            "certificate_file"
        ]
        