from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
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


    

