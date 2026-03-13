from rest_framework import serializers
from .models import Doubt,Reply

class ReplySerializer(serializers.ModelSerializer):
    
    upvote_count=serializers.SerializerMethodField()

    class Meta:
        model=Reply
        fields=[
            "id",
            "user",
            "answer",
            "upvote_count",
            "created_at"
        ]
        read_only_fields=["user"]

    def get_upvote_count(self,obj):
        return obj.upvotes.count()
        

class DoubtSerializer(serializers.ModelSerializer):

    replies=ReplySerializer(many=True,read_only=True)

    class Meta:
        model=Doubt
        fields=[
            "id",
            "lesson",
            "student",
            "question",
            "status",
            "created_at",
            "replies"
        ]
        read_only_fields=["student"]
