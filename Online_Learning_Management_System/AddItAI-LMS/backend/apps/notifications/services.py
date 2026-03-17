from .models import Notification

def create_notification(user,title,message,ntype="SYSTEM",actor=None,url=None):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=ntype,
        actor=actor,
        redirect_url=url
    )

