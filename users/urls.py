from django.urls import path
from users.views import PaymentsListAPIView

app_name = "users"

urlpatterns = [
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),
]
