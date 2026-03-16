from click import password_option
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, CreateAPIView

from users.models import Payments, User
from users.serialaizers import UserSerializer
from users.serializers import PaymentsSerializer


class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]

    ordering_fields = ["payment_date"]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = []

    def perform_create(self, serializer):
        user = serializer.save(is_active =True)
        user.set_password(user.password)
        user.save()
