from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.permissions import IsNotModeratorCreateDelete, IsOwner
from materials.serializers import (CourseSerializer, LessonDetailSerializer,
                                   LessonSerializer)


class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LessonDetailSerializer
        return LessonSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner(), IsNotModeratorCreateDelete()]

        if self.action == "create":
            return [IsAuthenticated(), IsNotModeratorCreateDelete()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseCreateAPIView(CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsNotModeratorCreateDelete]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="moderator").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)


class CourseRetrieveAPIView(RetrieveAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="moderator").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)


class CourseUpdateAPIView(UpdateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsNotModeratorCreateDelete]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="moderator").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)


class CourseDestroyAPIView(DestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsNotModeratorCreateDelete]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="moderator").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner(), IsNotModeratorCreateDelete()]

        if self.action == "create":
            return [IsAuthenticated(), IsNotModeratorCreateDelete()]

        return [IsAuthenticated()]
