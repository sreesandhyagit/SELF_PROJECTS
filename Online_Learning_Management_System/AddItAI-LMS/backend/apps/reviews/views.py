from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg
from .models import Review
from .serializers import ReviewSerializer
from apps.courses.models import Course
from apps.enrollments.models import Enrollment

# Create your views here.

class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        course_id=self.request.query_params.get("course")
        if course_id:
            return Review.objects.filter(course_id=course_id)
        return Review.objects.all()
    
    def perform_create(self, serializer):
        course=serializer.validated_data["course"]

        #allow review only if enrolled
        enrolled=Enrollment.objects.filter(user=self.request.user,course=course).exists()
        if not enrolled:
            raise PermissionError("You must enroll to review this course")
        serializer.save(user=self.request.user)

    #course rating summary
    @action(detail=False,methods=["get"])
    def course_rating(self,request):
        course_id=request.query_params.get("course")
        if not course_id:
            return Response({"error":"course id required"})
        rating=Review.objects.filter(course_id=course_id).aggregate(
            avg_rating=Avg("rating"),
            total_reviews=Avg("id")
        )
        return Response({
            "course":course_id,
            "average_rating":rating["avg_rating"],
            "total_reviews":Review.objects.filter(course_id=course_id).count()            
        })
    
    #my reviews
    @action(detail=False,methods=["get"])
    def my_reviews(self,request):
        reviews=Review.objects.filter(user=request.user)
        serializer=self.get_serializer(reviews, many=True)
        return Response(serializer.data)
    