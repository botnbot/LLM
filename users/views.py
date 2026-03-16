from rest_framework.viewsets import ModelViewSet

from materials.models import Course
from materials.serializers import CourseSerializer

from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from users.models import Payments
from users.serializers import PaymentsSerializer



class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ["paid_course", "paid_lesson", "payment_method"]

    ordering_fields = ["payment_date"]
