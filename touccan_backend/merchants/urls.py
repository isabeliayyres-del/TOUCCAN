from rest_framework.routers import DefaultRouter
from .views import MerchantViewSet

router = DefaultRouter()
router.register(r'', MerchantViewSet)

urlpatterns = router.urls