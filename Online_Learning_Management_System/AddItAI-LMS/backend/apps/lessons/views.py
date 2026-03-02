from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count,Q
from .models import Section,Lesson,LessonProgress
from .serializers import SectionSerializer,LessonSerializer,LessonProgressSerializer

# Create your views here.

class SectionViewSet(ModelViewSet):    
    queryset=Section.objects.all().order_by("order")
    serializer_class=SectionSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        #instructor sees only their sections
        return Section.objects.filter(course__instructor=user)
    
    def perform_create(self, serializer):
        course=serializer.validated_data.get("course")
        #check ownership
        if course.instructor!=self.request.user:
            raise PermissionDenied("You can only add sections to your own courses")
        serializer.save()

    def perform_update(self, serializer):
        section=self.get_object()
        if section.course.instructor!=self.request.user:
            raise PermissionDenied("Not allowed")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.course.instructor!=self.request.user:
            raise PermissionDenied("Not allowed")
        instance.delete()

    @action(detail=True,methods=["post"])
    def add_lesson(self,request,pk=None):
        section=self.get_object()

        if section.course.instructor!=request.user:
            raise PermissionDenied("Not allowed")
        
        serializer=LessonSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(section=section)#auto assign section
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#----------------------------------------------------------------------------------------------------------------------
class LessonViewSet(ModelViewSet):
    queryset=Lesson.objects.all().order_by("order")
    serializer_class=LessonSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Lesson.objects.filter(section__course__instructor=user)
    
    def perform_create(self, serializer):
        section=serializer.validated_data.get("section")
        if section.course.instructor!=self.request.user:
            raise PermissionDenied("Not your course")
        serializer.save()

    def perform_update(self, serializer):
        lesson=self.get_object()
        if lesson.section.course.instructor!=self.request.user:
            raise PermissionDenied("Not allowed")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.section.course.instructor!=self.request.user:
            raise PermissionDenied("Not allowed")
        instance.delete()

    @action(detail=True,methods=["get"])
    def player(self,request,pk=None):
        lesson=self.get_object()
        section=lesson.section

        prev_lesson=section.lessons.filter(order__lt=lesson.order).order_by("-order").first()

        if not prev_lesson:
            prev_section=lesson.section.course.sections.filter(order__lt=section.order).order_by("-order").first()
            if prev_section:
                prev_lesson=prev_section.lessons.order_by("-order").first()
        
        next_lesson=section.lessons.filter(order__gt=lesson.order).order_by("order").first()

        if not next_lesson:
            next_section=lesson.section.course.sections.filter(order__gt=section.order).order_by("order").first()
            if next_section:
                next_lesson=next_section.lessons.order_by("order").first()

        data={
            "current_lesson":{
                "id":lesson.id,
                "title":lesson.title,
                "youtube_url":lesson.youtube_url,
                "duration":lesson.get_duration_display()
            },
            "previous_lesson":{
                "id": prev_lesson.id,
                "title": prev_lesson.title,
                "youtube_url":prev_lesson.youtube_url
            } if prev_lesson else None,
            "next_lesson":{
                "id":next_lesson.id,
                "title":next_lesson.title,
                "youtube_url":next_lesson.youtube_url
            } if next_lesson else None,            
        }
        return Response(data)
    
#--------------------------------------------------------------------------------------------------------------
    
class LessonProgressViewSet(ModelViewSet):
    serializer_class=LessonProgressSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return LessonProgress.objects.filter(user=self.request.user)
    
    def create(self, request,*args,**kwargs):
        lesson=request.data.get("lesson")
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
        lessons=Lesson.objects.filter(section__course_id=course_id)
        total_lessons=lessons.count()
        completed=LessonProgress.objects.filter(user=request.user,lesson__in=lessons,is_completed=True).count()
        progress=(completed / total_lessons * 100) if total_lessons > 0 else 0
        return Response({
            "total_lessons":total_lessons,
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
        ).order_by("-last_watched_at").first()
        
        if not last: 
            return Response({"message":"No resume data"})
        
        return Response({
            "lesson_id":last.lesson.id,
            "lesson_title":last.lesson.title,
            "watched_duration":last.watched_duration
        })



    

