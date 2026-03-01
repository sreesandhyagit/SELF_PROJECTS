from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from apps.accounts.permissions import IsInstructor,IsAdmin
from .models import Course
from .serializers import CourseSerializer
from apps.lessons.serializers import SectionSerializer

# Create your views here.

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "slug"

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    #filtering
    filterset_fields = {
        'category__slug':['exact'],
        'price':['exact','gte','lte'],
        'level':['exact'],
        'is_published':['exact']
    }
    #search
    search_fields = ['title','description']
    #ordering
    ordering_fields = ['price','created_at','duration']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsInstructor()]
        elif self.action in ["update","partial_update","destroy"]:
            return [IsAuthenticated(),IsInstructor()]
        elif self.action in ["approve_course","reject_course","publish_course"]:
            return [IsAuthenticated(),IsAdmin()]        
        elif self.action == "add_section":
            return [IsAuthenticated(),IsInstructor()]
        return [AllowAny()]

    def perform_create(self,serializer):
        #when instructor creates,send for approval
        serializer.save(instructor=self.request.user,status=Course.Status.PENDING)

    def get_queryset(self):
        user = self.request.user
        queryset=Course.objects.all().prefetch_related("sections__lessons")

        if user.is_authenticated:
            if user.is_instructor:
                return queryset.filter(instructor=user)
            elif user.is_admin:
                return queryset
            
        return queryset.filter(status=Course.Status.APPROVED,is_published=True)

    #approve
    @action(detail=True,methods=["post"])
    def approve_course(self,request,slug=None):
        course = self.get_object()
        course.status = Course.Status.APPROVED
        course.save()
        return Response({"message":"Course approved"},status=status.HTTP_200_OK)
    
    #reject
    @action(detail=True,methods=["post"])
    def reject_course(self,request,slug=None):
        course = self.get_object()
        course.status = Course.Status.REJECTED
        course.save()
        return Response({"message":"Course rejected"},status=status.HTTP_200_OK)

    #publish/unpublish
    @action(detail=True,methods=["post"])
    def publish_course(self,request,slug=None):
        course = self.get_object()
        if course.status != Course.Status.APPROVED:
            return Response(
                {"error":"Only approved courses can be published"},
                status=status.HTTP_400_BAD_REQUEST
            )
        course.is_published = not course.is_published
        course.save()
        return Response({
            "message":"Course published" if course.is_published else "Course unpublished"
            })
    
    @action(detail=True,methods=["post"])
    def add_section(self,request,slug=None):
        course=self.get_object()
        if course.instructor!=request.user:
            raise PermissionDenied("Not allowed")
        serializer=SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
