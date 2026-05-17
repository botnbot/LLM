from django.contrib.auth.hashers import make_password
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
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Payments, User
from users.permissions import IsOwner
from users.serializers import (
    PaymentsSerializer,
    UserSerializer,
    MyTokenObtainPairSerializer,
)
from users.service import create_stripe_session, create_stripe_price


#  CRUD пользователей


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


#  Регистрация пользователя


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(
            password=make_password(serializer.validated_data["password"]),
            is_active=True,
        )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Платежи


class PaymentsListAPIView(ListAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payments.objects.filter(user=self.request.user)

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]
    ordering_fields = ["payment_date"]


class PaymentsCreateAPIView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        item = payment.get_paid_item()
        if not item:
            raise ValueError("Не указан курс или урок")
        amount = payment.payment_amount
        price = create_stripe_price(amount )
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

