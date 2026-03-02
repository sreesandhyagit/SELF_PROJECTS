from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count,Q
from .models import Section,Lesson
from .serializers import SectionSerializer,LessonSerializer

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

    




    

