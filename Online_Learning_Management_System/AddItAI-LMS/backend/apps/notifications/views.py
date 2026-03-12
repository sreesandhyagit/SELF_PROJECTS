from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.

class NotificationViewSet(ModelViewSet):
    serializer_class=NotificationSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
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
    
