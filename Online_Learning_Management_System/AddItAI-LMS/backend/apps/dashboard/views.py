from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum,Avg,Count
from apps.accounts.models import User
from apps.courses.models import Course
from apps.enrollments.models import Enrollment
from apps.orders.models import Order
from apps.reviews.models import Review
from apps.doubts.models import Doubt
from apps.progress.models import LessonProgress
from apps.certificates.models import Certificate
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncMonth


# Create your views here.

class AdminDashboardView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        data={
            "total_users":User.objects.count(),
            "students":User.objects.filter(role="STUDENT").count(),
            "instructors":User.objects.filter(role="INSTRUCTOR").count(),
            "pending_instructors":User.objects.filter(role="INSTRUCTOR",is_instructor_approved=False).count(),
            "total_courses":Course.objects.count(),
            "pending_courses":Course.objects.filter(status="PENDING").count(),
            "approved_courses":Course.objects.filter(status="APPROVED").count(),
            "published_courses":Course.objects.filter(is_published=True).count(),
            "total_enrollments":Enrollment.objects.count(),
            "total_orders":Order.objects.count(),
            "total_revenue":Order.objects.filter(status="PAID").aggregate(total=Sum("amount"))["total"] or 0,
            "reviews":Review.objects.count(),
            "open_doubts":Doubt.objects.filter(status="OPEN").count()
        }
        return Response(data)
    
    
class InstructorDashboardView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        instructor=request.user

        if request.user.role != "INSTRUCTOR":
            return Response({"error":"Only Instructor allowed"},status=403)
        
        courses=Course.objects.filter(instructor=instructor)
        enrollments=Enrollment.objects.filter(course__instructor=instructor)

        revenue=Order.objects.filter(
            course__instructor=instructor,
            status="PAID"
        ).aggregate(total=Sum("amount"))["total"] or 0

        avg_rating=Review.objects.filter(
            course__instructor=instructor
        ).aggregate(avg=Avg("rating"))["avg"] or 0

        data={
            "my_courses":courses.count(),
            "pending_courses":courses.filter(status="PENDING").count(),
            "approved_courses":courses.filter(status="APPROVED").count(),
            "published_courses":courses.filter(is_published=True).count(),
            "total_students":enrollments.count(),
            "revenue":revenue,
            "average_rating":round(avg_rating,2),
            "pending_doubts":Doubt.objects.filter(lesson__section__course__instructor=instructor,status="OPEN").count()
        }
        return Response(data)
    

class StudentDashboardView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user=request.user
        enrollments=Enrollment.objects.filter(user=user)
        completed_lessons=LessonProgress.objects.filter(user=user,is_completed=True).count()
        certificates=Certificate.objects.filter(user=user)
        data={
            "enrolled_courses":enrollments.count(),
            "completed_lessons":completed_lessons,
            "completed_courses":certificates.count(),
            "certificates":certificates.count(),
            "my_doubts":Doubt.objects.filter(user=user).count(),
            "my_reviews":Review.objects.filter(user=user).count()
        }
        return Response(data)
    

class InstructorRequestListView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        requests=User.objects.filter(role="INSTRUCTOR",is_instructor_approved=False)
        data=requests.values("id","username","email","date_joined")
        return Response(data)
    
    
class ApproveInstructorView(APIView):
    permission_classes=[IsAdminUser]
    
    def post(self,request,id):
        user=get_object_or_404(User,id=id)
        user.is_instructor_approved=True
        user.role="INSTRUCTOR"
        user.save()
        return Response({"message":"Instructor approved"})
    
    
class RejectInstructorView(APIView):
    permission_classes=[IsAdminUser]

    def post(self,request,id):
        user=get_object_or_404(User,id=id)
        user.role="STUDENT"
        user.is_instructor_approved=False
        user.save()
        return Response({"message":"Instructor rejected"})
    
    
class PendingCoursesView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        courses=Course.objects.filter(status="PENDING")
        data=courses.values("title","instructor__email","created_at")
        return Response(data)
    

class ApproveCourseView(APIView):
    permission_classes=[IsAdminUser]

    def post(self,request,slug):
        course=get_object_or_404(Course,slug=slug)
        course.status="APPROVED"
        course.save()
        return Response({"message":"Course Approved"})
    

class RejectCourseView(APIView):
    permission_classes=[IsAdminUser]

    def post(self,request,slug):
        course=get_object_or_404(Course,slug=slug)
        course.status="REJECTED"
        course.save()
        return Response({"message":"Course rejected"})


class AdminAnalyticsView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        top_courses=Course.objects.annotate(
            students=Count("enrollment")
        ).order_by("-students")[:5]

        top_instructors=User.objects.filter(
            role="INSTRUCTOR"
        ).annotate(
            courses_count=Count("course")
        ).order_by("-courses_count")[:5]

        data={
            "top_courses":list(top_courses.values("title","students")),
            "top_instructors":list(top_instructors.values("username","courses_count"))
        }
        return Response(data)
    

class StudentLearningStatus(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        completed=LessonProgress.objects.filter(user=user,is_completed=True).count()
        total=LessonProgress.objects.filter(user=user).count()
        progress=0
        if total>0:
            progress=(completed/total)*100
        return Response({
            "completed_lessons":completed,
            "total_lessons":total,
            "progress_percentage":round(progress,2)
        })
    

class CoursePopularityView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        courses=Course.objects.annotate(
            students=Count("enrollment")
        ).order_by("-students")

        return Response(courses.values("title","students"))
    

class RecentEnrollmentsView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        enrollments=Enrollment.objects.order_by("-created_at")[:10]
        data=enrollments.values("user__email","course__title","created_at")
        return Response(data)
    

class RecentOrdersView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        orders=Order.objects.order_by("-created_at")[:10]
        data=orders.values("user__email","course__title","amount","status","created_at")
        return Response(data)
    

class RecentReviewsView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        reviews=Review.objects.order_by("-created_at")[:10]
        data=reviews.values("user__email","course__title","rating","created_at")
        return Response(data)
    

class MonthlyRevenueView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        revenue=Order.objects.filter(
            status="PAID"
        ).annotate(
            month=TruncMonth("created_at")
        ).values("month").annotate(
            total=Sum("amount")
        ).order_by("month")
        return Response(revenue)
    

class InstructorCourseRevenueView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        instructor=request.user

        if instructor.role != "INSTRUCTOR":
            return Response({"error":"Only instructor allowed"},status=403)
        
        courses=Course.objects.filter(instructor=instructor).annotate(
            total_students=Count("enrollments"),
            total_revenue=Sum("order__amount")
        )
        data=courses.values("title","total_students","total_revenue")
        return Response(data)
    

class InstructorPayoutView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        instructor=request.user

        if instructor.role != "INSTRUCTOR":
            return Response({"error":"Only instructor allowed"},status=403)
        
        courses=Course.objects.filter(instructor=instructor).annotate(
            students=Count("enrollments"),
            total_revenue=Sum("order__amount")
        )
        result=[]
        for course in courses:
            total=course.total_revenue or 0
            instructor_share=total*0.70
            platform_share=total*0.30

            result.append({
                "course":course.title,
                "students":course.students,
                "total_revenue":total,
                "instructor_earning":round(instructor_share,2),
                "platform_share":round(platform_share,2)
            })
        return Response(result)
        

