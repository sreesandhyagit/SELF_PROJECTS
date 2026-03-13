from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Certificate
from .serializers import CertificateSerializer
from apps.progress.models import LessonProgress
from apps.lessons.models import Lesson
from apps.courses.models import Course
from apps.enrollments.models import Enrollment
from .services import generate_certificate
from apps.notifications.services import create_notification
from django.shortcuts import get_object_or_404

# Create your views here.

class CertificateViewSet(ModelViewSet):
    serializer_class=CertificateSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user)

    @action(detail=False,methods=["post"])
    def generate(self,request):
        course_id=request.data.get("course")
        # course=Course.objects.filter(id=course_id).first()
        course=get_object_or_404(Course,id=course_id)
        if not course:
            return Response({"error":"Course not found"})
        
        if not course.is_published or course.status != "APPROVED":
            return Response({"error":"Course not available"})
        
        is_enrolled=Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

        if not is_enrolled:
            return Response({"error":"You are not enrolled in this course"},status=403)
                
        total_lessons=Lesson.objects.filter(section__course=course).count()
        completed_lessons=LessonProgress.objects.filter(
            user=request.user,
            lesson__section__course=course,
            is_completed=True            
        ).count()
        if completed_lessons < total_lessons:
            return Response({"error":"Course not completed yet"})
        
        certificate, created=Certificate.objects.get_or_create(
            user=request.user,
            course=course
        )
        if created or not certificate.certificate_file:
            file_path=generate_certificate(request.user,course,certificate)            
            certificate.certificate_file=file_path
            certificate.save()
        serializer=self.get_serializer(certificate)

        create_notification(
            user=request.user,
            title="Certificate Ready",
            message=f"Your certificate for {course.title} is ready to download",
            ntype="CERTIFICATE"
        )
        return Response(serializer.data)
    
            