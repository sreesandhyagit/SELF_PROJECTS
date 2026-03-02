from rest_framework.routers import DefaultRouter
from .views import SectionViewSet,LessonViewSet,LessonProgressViewSet

router=DefaultRouter()
router.register("sections",SectionViewSet)
router.register("lessons",LessonViewSet)
router.register(r"progress",LessonProgressViewSet,basename="progress")

urlpatterns = router.urls
