from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payments, User
from users.permissions import IsSelf
from users.serializers import (PaymentsSerializer, UserProfileSerializer,
                               UserSerializer)


class PaymentsListAPIView(ListAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]

    ordering_fields = ["payment_date"]

    def get_queryset(self):
        return Payments.objects.filter(user=self.request.user)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserProfileSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsSelf()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
