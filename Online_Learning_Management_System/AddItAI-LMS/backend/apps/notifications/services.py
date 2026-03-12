from .models import Notification

def create_notification(user,title,message,ntype="SYSTEM"):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=ntype
    )

