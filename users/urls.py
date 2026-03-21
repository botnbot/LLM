from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import PaymentsListAPIView, UserViewSet

app_name = "users"

router = SimpleRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),
]
urlpatterns += router.urls
