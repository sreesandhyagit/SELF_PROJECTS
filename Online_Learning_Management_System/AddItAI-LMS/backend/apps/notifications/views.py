from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from apps.accounts.models import User
from apps.notifications.services import create_notification
from .pagination import NotificationPagination

# Create your views here.

class NotificationViewSet(ModelViewSet):
    serializer_class=NotificationSerializer
    permission_classes=[IsAuthenticated]
    pagination_class = NotificationPagination

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user)

        ntype = self.request.query_params.get("type")
        if ntype:
            qs = qs.filter(notification_type=ntype)

        return qs.order_by("-created_at")
    
    #mark notification as read
    @action(detail=True,methods=["post"])
    def mark_read(self,request,pk=None):
        notification=self.get_object()
        notification.is_read=True
        notification.save()
        return Response({"message":"Notification marked as read"})
    
    #mark all as read
    @action(detail=False,methods=["post"])
    def mark_all_read(self,request):
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        return Response({"message":"All notifications marked as read"})
    
    #unread count
    @action(detail=False,methods=["get"])
    def unread_count(self,request):
        count=Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        return Response({"unread_notifications":count})
    
class BroadcastNotificationView(APIView):
    permission_classes=[IsAdminUser]

    def post(self,request):
        users = User.objects.all()
        title = request.data.get("title")
        message = request.data.get("message")
        notifications = [
            Notification(
                user=user,
                title=title,
                message=message
            )
            for user in users
        ]
        Notification.objects.bulk_create(notifications)
        return Response({"message":"Notification sent to all users"})