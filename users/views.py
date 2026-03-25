from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payments, User
from users.serializers import PaymentsSerializer, UserSerializer

#  CRUD пользователей


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


#  Регистрация пользователя


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = []

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data["password"])
        user.save()


# Платежи


class PaymentsListAPIView(ListAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payments.objects.filter(user=self.request.user)

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["payment_date"]
