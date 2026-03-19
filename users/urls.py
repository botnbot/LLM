from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentsListAPIView,
    UserCreateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    #  Регистрация
    path("register/", UserCreateAPIView.as_view(), name="register"),
    #  JWT
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=[AllowAny]),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=[AllowAny]),
        name="token_refresh",
    ),
    #  CRUD пользователей
    path("users/", UserListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="users_retrieve"),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="users_update"),
    path("users/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="users_delete"),
    #  Платежи
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),
]
