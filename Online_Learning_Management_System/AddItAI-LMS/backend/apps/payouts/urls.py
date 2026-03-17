from django.urls import path
from .views import *

urlpatterns = [
    path("request/",RequestPayoutView.as_view()),
    path("history/",InstructorPayoutHistoryView.as_view()),
    path("admin/pending/",PendingPayoutsView.as_view()),
    path("admin/approve/<int:id>/",ApprovePayoutView.as_view()),
    path("admin/paid/<int:id>/",MarkPayoutPaidView.as_view())
    
]
