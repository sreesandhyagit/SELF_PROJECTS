from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count,Q
from .models import Section,Lesson
from apps.progress.models import LessonProgress
from apps.courses.models import Course
from .serializers import SectionSerializer,LessonSerializer
from apps.enrollments.models import Enrollment

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
    
    @action(detail=False,methods=["get"])
    def section_progress(self, request):
        course_id=request.query_params.get("course_id")

        if not course_id:
            return Response({"error":"course_id required"},status=400)
        
        sections=Section.objects.filter(course_id=course_id).annotate(
            total_lessons=Count("lessons"),
            completed_lessons=Count(
                "lessons__progress",
                filter=Q(
                    lessons__progress__user=request.user,
                    lessons__progress__is_completed=True
                )
            )
        )
        data=[]
        for section in sections:
            progress=(
                section.completed_lessons /section.total_lessons * 100
                if section.total_lessons > 0 else 0
            )
            data.append({
                "section_id":section.id,
                "section_title":section.title,
                "total_lessons":section.total_lessons,
                "completed_lessons":section.completed_lessons,
                "progress":round(progress,2)
            })
            return Response(data)
        
    
#----------------------------------------------------------------------------------------------------------------------
class LessonViewSet(ModelViewSet):
    queryset=Lesson.objects.all().order_by("order")
    serializer_class=LessonSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        #allow player endpoint to access all lessons
        if self.action == "player":
            return Lesson.objects.all()
        
        #instructor - their lessons
        if user.is_instructor:
            return Lesson.objects.filter(section__course__instructor=user)
        
        #students -published courses
        return Lesson.objects.filter(
            section__course__is_published=True,
            section__course__status="APPROVED"
        )
    
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
        course=lesson.section.course
        user=request.user

        #block unpublished course
        if not course.is_published or course.status != "APPROVED":
            return Response({"error":"Course not available"},status=403)
        
        #paid course check  
        if not lesson.is_preview and not course.is_free:
                is_enrolled=Enrollment.objects.filter(user=user,course=course).exists()
                if not is_enrolled:
                    return Response({"error":"You must enroll to access this lesson"},status=403)

          
        #navigation part

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

        #unlock next lesson only if completed
        if next_lesson:
            is_completed=LessonProgress.objects.filter(user=user,lesson=lesson,is_completed=True).exists()

            if not is_completed:
                next_lesson=None 

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
            } if next_lesson else None
        }  

        return Response(data)
    
    @action(detail=True,methods=["post"])
    def complete(self,request,pk=None):
        lesson=self.get_object()
        user=request.user        
        course=lesson.section.course

        #block unpublished course
        if not course.is_published or course.status != "APPROVED":
            return Response({"error":"Course not available"},status=403)
        
        #prevent unauthorized completeion
        if not lesson.is_preview and not course.is_free:
            is_enrolled=Enrollment.objects.filter(user=user,course=course).exists()
            if not is_enrolled:
                return Response({"error":"Enroll first"},status=403)
        
        progress, created =LessonProgress.objects.get_or_create(user=user,lesson=lesson)

        progress.is_completed=True
        progress.save()

        return Response({"message":"Lesson Completed"})

    @action(detail=True,methods=["post"])
    def next_lesson(self,request,pk=None):
        lesson=self.get_object()
        section=lesson.section

        next_lesson=section.lessons.filter(order__gt=lesson.order).order_by("order").first()
        if not next_lesson:
            next_section=lesson.section.course.sections.filter(
                order__gt=section.order
            ).order_by("order").first()

            if next_section:
                next_lesson=next_section.lessons.order_by("order").first()
        
        if not next_lesson:
            return Response({"message":"Course Completed"})
        
        return Response({
            "next_lesson_id":next_lesson.id,
            "title":next_lesson.title,
            "video_url":next_lesson.youtube_url
        })

    @action(detail=False,methods=["get"])
    def recommendations(self,request):
        #get users completed lessons
        completed_lessons=LessonProgress.objects.filter(
            user=request.user,
            is_completed=True
        ).values_list("lesson__section__course__category", flat=True)

        #recommend courses from same category
        courses =Course.objects.filter(
            category__in=completed_lessons,
            is_published=True,
            status="APPROVED"
        ).distinct()[:5]

        data=[
            {
                "id":c.id,
                "title":c.title,
                "price":c.price
            }
            for c in courses
        ]
        return Response(data)
    




    

