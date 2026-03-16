from django.urls import path
from .views import *

urlpatterns = [

    #admin dashboard
    path("admin/dashboard/",AdminDashboardView.as_view()),
    path("admin/analytics/",AdminAnalyticsView.as_view()),
    path("admin/monthly-revenue/",MonthlyRevenueView.as_view()),
    path("admin/course-popularity/", CoursePopularityView.as_view()),
    path("admin/recent-enrollments/",RecentEnrollmentsView.as_view()),
    path("admin/recent-orders/",RecentOrdersView.as_view()),
    path("admin/recent-reviews/",RecentReviewsView.as_view()),
    
    #instructor dashboard
    path("instructor/dashboard/",InstructorDashboardView.as_view()),
    path("instructor/payouts/",InstructorPayoutView.as_view()),
    path("instructor/course-revenue/",InstructorCourseRevenueView.as_view()),

    #student dashboard
    path("student/dashboard/",StudentDashboardView.as_view()),
    path("student/progress/",StudentLearningStatus.as_view()),

    #admin moderation
    path("admin/instructor-requests/",InstructorRequestListView.as_view()),
    path("admin/instructor-approve/<int:id>/",ApproveInstructorView.as_view()),
    path("admin/instructor-reject/<int:id>/",RejectInstructorView.as_view()),

    path("admin/pending-courses/",PendingCoursesView.as_view()),
    path("admin/course-approve/<slug:slug>/",ApproveCourseView.as_view()),
    path("admin/course-reject/<slug:slug>/",RejectCourseView.as_view()),

]
