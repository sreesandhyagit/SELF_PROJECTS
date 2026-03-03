from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count,Q
from .models import Lesson,LessonProgress
from .serializers import LessonProgressSerializer


# Create your views here.

class LessonProgressViewSet(ModelViewSet):
    serializer_class=LessonProgressSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return LessonProgress.objects.filter(user=self.request.user)
    
    def create(self, request,*args,**kwargs):
        lesson=request.data.get("lesson")
        if not Lesson.objects.filter(id=lesson).exists():
            return Response({"error":"Invalid lesson"},status=400)
        try:
            obj = LessonProgress.objects.get(user=request.user,lesson_id=lesson)
            #update existing
            obj.watched_duration=request.data.get("watched_duration",obj.watched_duration)
            obj.is_completed=request.data.get("is_completed",obj.is_completed)
            obj.save()
            serializer=self.get_serializer(obj)
            return Response(serializer.data,status=200)
        except LessonProgress.DoesNotExist:
            serializer=self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data,status=201)

    #mark lesson as complete
    @action(detail=True,methods=["post"])
    def mark_complete(self,request,pk=None):
        progress=self.get_object()
        lesson=progress.lesson

        if progress.watched_duration >= lesson.duration:
            progress.is_completed=True

        progress.save()
        return Response({"message":"Lesson marked as completed"})
    
    #update watch time (resume feature)
    @action(detail=True,methods=["post"])
    def update_watch_time(self,request,pk=None):
        progress=self.get_object()
        seconds=int(request.data.get("watched_duration",0))
        if seconds < 0:
            return Response({"error":"Invalid duration"},status=400)
        progress.watched_duration=seconds
        progress.save()
        return Response({"message":"Watch time updated", "watched_duration":progress.watched_duration})
    
    #course progress
    @action(detail=False,methods=["get"])
    def course_progress(self,request):
        course_id=request.query_params.get("course_id")
        if not course_id:
            return Response({"error":"course_id required"},status=400)        

        lessons=Lesson.objects.filter(section__course__id=course_id).aggregate(
            total_lessons=Count("id"),
            completed_lessons=Count(
                "progress",
                filter=Q(progress__user=request.user,progress__is_completed=True),
                distinct=True
            )
        )
        total=lessons["total_lessons"]
        completed=lessons["completed_lessons"]
        progress=(completed / total * 100) if total > 0 else 0

        return Response({
            "total_lessons":total,
            "completed_lessons":completed,
            "progress_percentage":round(progress,2)
         })

    #resume learning
    @action(detail=False,methods=["get"])
    def resume(self,request):
        last=LessonProgress.objects.filter(
            user=request.user,
            watched_duration__gt=0,
            is_completed=False
        ).select_related("lesson","lesson__section__course") \
        .order_by("-last_watched_at") \
        .first()
        
        if not last: 
            last=LessonProgress.objects.filter(
                user=request.user,
                is_completed=True
            ).order_by("-last_watched_at").first()

            if not last:
                return Response({"message":"No resume data"})
        
        return Response({
            "lesson_id":last.lesson.id,
            "lesson_title":last.lesson.title,
            "course":last.lesson.section.course.title,
            "watched_duration":last.watched_duration,
            "video_url":last.lesson.youtube_url
        })