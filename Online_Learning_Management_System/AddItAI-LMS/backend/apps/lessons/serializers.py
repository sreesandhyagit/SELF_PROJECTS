from rest_framework import serializers
from .models import Section,Lesson
import re

def convert_to_seconds(time_str):
    try:
        h,m,s=map(int,time_str.split(":"))
        return h * 3600 + m * 60 + s
    except:
        raise serializers.ValidationError("Invalid format. Use HH:MM:SS")
    

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Section
        fields="__all__"

class LessonSerializer(serializers.ModelSerializer):
    duration_input=serializers.CharField(write_only=True)
    duration_display=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model=Lesson
        fields=[
            "id",
            "section",
            "title",
            "slug",
            "youtube_url",
            "duration",
            "duration_input",
            "duration_display",
            "thumbnail",
            "order",
            "is_preview"
        ]
        extra_kwargs={"section":{"required":False}}
        read_only_fields=["slug","duration"]

    def get_duration_display(self,obj):
        return obj.get_duration_display()
    
    def validate_youtube_url(self,value):
        if "youtube.com" not in value and "youtu.be" not in value:
            raise serializers.ValidationError("Only youtube links allowed")
        #enforce unlisted
        if "watch?v=" not in value and "youtu.be" not in value:
            raise serializers.ValidationError("Use valid youtube link")
        return value
    
    def create(self, validated_data):
        duration_input = validated_data.pop("duration_input")
        validated_data["duration"]=convert_to_seconds(duration_input)        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if "duration_input" in validated_data:
            duration_input = validated_data.pop("duration_input")
            instance.duration=convert_to_seconds(duration_input)
        return super().update(instance, validated_data)

class SectionWithLessonsSerializer(serializers.ModelSerializer):
    lessons=LessonSerializer(many=True,read_only=True)
    class Meta:
        model=Section
        fields=["id","title","order","lessons"]
        