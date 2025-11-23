from rest_framework.routers import DefaultRouter
from .views import LeadStatusViewSet, LeadsViewSet

router = DefaultRouter()
router.register(r'lead-status', LeadStatusViewSet)
router.register(r'leads', LeadsViewSet)

urlpatterns = router.urls