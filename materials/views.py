from rest_framework import viewsets
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    LessonDetailSerializer,
)
from users.permissions import IsModerator, IsOwner


# Lesson ViewSet


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LessonDetailSerializer
        return LessonSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "retrieve"]:
            return [IsAuthenticated(), IsModerator() | IsOwner()]
        elif self.action == "create":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


# Course Generic Views


class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)


class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModerator() | IsOwner]


class CourseUpdateAPIView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModerator() | IsOwner]


class CourseDestroyAPIView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModerator() | IsOwner]


# Course ViewSet


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "retrieve"]:
            return [IsAuthenticated(), IsModerator() | IsOwner()]
        elif self.action == "create":
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)
