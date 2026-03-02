from rest_framework import serializers
from .models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enrollment
        fields=["id","course","is_active","enrolled_at"]
        read_only_fields=["enrolled_at"]
        