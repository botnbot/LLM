from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseCreateAPIView,
    CourseDestroyAPIView,
    CourseListAPIView,
    CourseRetrieveAPIView,
    CourseUpdateAPIView,
    LessonViewSet,
    SubscriptionAPIView,
)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("lessons", LessonViewSet, basename="lessons")

urlpatterns = [
    path("courses/", CourseListAPIView.as_view(), name="courses_list"),
    path("courses/<int:pk>/", CourseRetrieveAPIView.as_view(), name="courses_retrieve"),
    path("courses/create/", CourseCreateAPIView.as_view(), name="courses_create"),
    path(
        "courses/<int:pk>/delete/",
        CourseDestroyAPIView.as_view(),
        name="courses_delete",
    ),
    path(
        "courses/<int:pk>/update/", CourseUpdateAPIView.as_view(), name="courses_update"
    ),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
]

urlpatterns += router.urls
