from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('touccan/v1/', include([
        path('users/', include('users.urls')),
        path('merchants/', include('merchants.urls')),
        path('products/', include('products.urls')),
        path('orders/', include('orders.urls')),
        path('carts/', include('carts.urls')),
    ]))
]

urlpatterns += [
    path('touccan/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('touccan/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
