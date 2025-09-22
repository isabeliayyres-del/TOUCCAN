from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthenticationView, UserProfileView, ChangePasswordView, LogoutView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/register/', AuthenticationView.as_view(), name='user-register'),
    path('api/auth/login/', AuthenticationView.as_view(), name='user-login'),
    path('api/auth/logout/', LogoutView.as_view(), name='user-logout'),
    path('api/auth/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
]

app_name = 'users'
