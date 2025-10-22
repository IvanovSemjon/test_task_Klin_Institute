from rest_framework import routers
from .views import WorkerViewSet


router = routers.DefaultRouter()
router.register(r"workers", WorkerViewSet, basename="worker")

urlpatterns = router.urls
