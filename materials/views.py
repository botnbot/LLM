from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson
from materials.paginators import StandardResultsSetPagination
from materials.serializers import CourseSerializer, LessonSerializer, LessonDetailSerializer
from users.models import Subscription
from users.permissions import IsModeratorOrOwner


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LessonDetailSerializer
        return LessonSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "retrieve"]:
            return [IsAuthenticated(), IsModeratorOrOwner()]
        elif self.action == "create":
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.groups.filter(name="Moderators").exists():
    #         return Lesson.objects.all()
    #     return Lesson.objects.filter(owner=user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(
            Q(owner=user) | Q(owner__isnull=True)
        )


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
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)


class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]


class CourseUpdateAPIView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]


class CourseDestroyAPIView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]


# # Course ViewSet
# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     pagination_class = StandardResultsSetPagination
#
#     def get_permissions(self):
#         if self.action in ["update", "partial_update", "destroy", "retrieve"]:
#             return [IsAuthenticated(), IsModerator() | IsOwner()]
#         elif self.action == "create":
#             return [IsAuthenticated()]
#         return [IsAuthenticated()]
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#     def get_queryset(self):
#         user = self.request.user
#         if user.groups.filter(name="Moderators").exists():
#             return Course.objects.all()
#         return Course.objects.filter(owner=user)


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    COURSE_ID_FIELD = "course_id"

    def post(self, request):
        user = request.user
        course_id = request.data.get(self.COURSE_ID_FIELD)

        if not course_id:
            return Response(
                {"error": "course_id обязателен"},
                status=400
            )

        try:
            course_id = int(course_id)
        except (TypeError, ValueError):
            return Response(
                {"error": "course_id должен быть числом"},
                status=400
            )

        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(
            user=user,
            course=course
        )

        if not created:
            subscription.delete()
            return Response(
                {"message": "подписка удалена"},
                status=200
            )

        return Response(
            {"message": "подписка добавлена"},
            status=201
        )
