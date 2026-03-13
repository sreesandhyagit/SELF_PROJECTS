from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Doubt,Reply
from .serializers import DoubtSerializer,ReplySerializer
from apps.enrollments.models import Enrollment
from apps.notifications.services import create_notification

# Create your views here.

class DoubtViewSet(ModelViewSet):
    serializer_class=DoubtSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        lesson_id=self.request.query_params.get("lesson")
        if lesson_id:
            return Doubt.objects.filter(lesson_id=lesson_id)
        # return Doubt.objects.all()
        return Doubt.objects.select_related(
            "lesson",
            "lesson__section",
            "lesson__section__course"
        )
    
    def perform_create(self, serializer):
        lesson=serializer.validated_data["lesson"]
        course=lesson.section.course
        instructor=course.instructor
        is_enrolled=Enrollment.objects.filter(
            user=self.request.user,
            course=course
        ).exists()
        if not is_enrolled:
            raise PermissionDenied("You must enroll first")
        serializer.save(student=self.request.user)
        #notify instructor
        create_notification(
            user=instructor,
            title="New Doubt Posted",
            message=f"{self.request.user.username} asked a doubt in {lesson.title}",
            ntype="QNA"
        )

    #reply to doubt
    @action(detail=True,methods=["post"])
    def reply(self,request,pk=None):
        doubt=self.get_object()
        course_instructor=doubt.lesson.section.course.instructor
        if request.user != course_instructor:
            raise PermissionDenied("Only instructor can reply")
        serializer=ReplySerializer(data=request.data)
        if serializer.is_valid():
            reply=serializer.save(doubt=doubt,user=request.user)
            #notify student
            create_notification(
                user=doubt.student,
                title="Doubt Answered",
                message=f"Instructor replied to your doubt in {doubt.lesson.title}",
                ntype="QNA"
            )        
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    
    #upvote reply
    @action(detail=False,methods=["post"])
    def upvote(self,request):
        reply_id=request.data.get("reply_id")
        reply=Reply.objects.get(id=reply_id)
        reply.upvotes.add(request.user)
        create_notification(
            user=reply.user,
            title="Reply Upvoted",
            message=f"Your reply received an upvote",
            ntype="QNA"
        )
        return Response({"message":"Upvoted"})
    
    #mark resolved
    @action(detail=True,methods=["post"])
    def resolve(self,request,pk=None):
        doubt=self.get_object()
        if doubt.student != request.user:
            raise PermissionDenied("Only student can mark resolved")
        doubt.status="RESOLVED"
        doubt.save()
        instructor=doubt.lesson.section.course.instructor
        create_notification(
            user=instructor,
            title="Doubt Resolved",
            message=f"Doubt in {doubt.lesson.title} was marked resolved",
            ntype="QNA"
        )
        return Response({"message":"Doubt Resolved"})
    
    #student dashboard
    @action(detail=False,methods=["get"])
    def my_doubts(self,request):
        doubts=Doubt.objects.filter(student=request.user)
        serializer=self.get_serializer(doubts,many=True)
        return Response(serializer.data)
    
    #instructor pending doubts
    @action(detail=False,methods=["get"])
    def pending(self,request):
        if not request.user.is_instructor:
            raise PermissionDenied()
        doubts=Doubt.objects.filter(
            lesson__section__course__instructor=request.user,
            status="OPEN"
        )
        serializer=self.get_serializer(doubts,many=True)
        return Response(serializer.data)
    


