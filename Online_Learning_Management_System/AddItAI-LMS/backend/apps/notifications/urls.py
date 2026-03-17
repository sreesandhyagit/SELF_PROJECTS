# urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, BroadcastNotificationView

router = DefaultRouter()
router.register("notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    path("broadcast/", BroadcastNotificationView.as_view()),
]

urlpatterns += router.urls