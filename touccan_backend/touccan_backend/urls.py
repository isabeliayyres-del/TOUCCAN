from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('touccan/v1/users/', include('users.urls')),
    path('touccan/v1/merchants/', include('merchants.urls')),
    path('touccan/v1/products/', include('products.urls')),
    path('touccan/v1/orders/', include('orders.urls')),
]
