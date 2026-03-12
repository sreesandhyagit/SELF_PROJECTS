from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Enrollment
from .serializers import EnrollmentSerializer
from apps.courses.models import Course
from apps.notifications.services import create_notification

# Create your views here.

class EnrollmentViewSet(ModelViewSet):
    serializer_class=EnrollmentSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)
    
    def create(self,request,*args,**kwargs):
        course_id=self.request.data.get("course")
        try:
            course=Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error":"Course not found"},status=404)
        
        #auto enroll free course
        if course.is_free:
            enrollment, created = Enrollment.objects.get_or_create(user=request.user,course=course)
            create_notification(
                user=request.user,
                title="Course Enrolled",
                message=f"You successfully enrolled in {course.title}",
                ntype="ENROLLMENT"
            )
            return Response({"message":"Enrolled in free course"})
        else:
            #simulate payment -paid course
            payment_status=request.data.get("payment_status")
            if payment_status != "success":
                return Response({"error":"Payment required"},status=400)
            enrollment, created=Enrollment.objects.get_or_create(user=request.user,course=course)

        serializer=self.get_serializer(enrollment)

        create_notification(
            user=request.user,
            title="Course Enrolled",
            message=f"You successfully enrolled in {course.title}",
            ntype="ENROLLMENT"
        )

        return Response({
            "message":"Enrolled successfully",
            "data":serializer.data
            },status=status.HTTP_201_CREATED)
    
