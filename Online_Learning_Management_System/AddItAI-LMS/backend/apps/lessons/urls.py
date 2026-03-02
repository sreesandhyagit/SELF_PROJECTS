from rest_framework.routers import DefaultRouter
from .views import SectionViewSet,LessonViewSet

router=DefaultRouter()
router.register("sections",SectionViewSet)
router.register("lessons",LessonViewSet)

urlpatterns = router.urls
