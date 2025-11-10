from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, PaymentMethodViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'payment-methods', PaymentMethodViewSet, basename='payment-method')

urlpatterns = [
    path('', include(router.urls)),
]

