# from django.urls import path
# from .views import OrderViewSet, OrderDetailView

# urlpatterns = [
#     path('', OrderViewSet.as_view(), name='order-list'),
#     path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
# ] 
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'', OrderViewSet)  # registra sem prefixo adicional

urlpatterns = router.urls
