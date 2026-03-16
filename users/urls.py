from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, UserCreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]