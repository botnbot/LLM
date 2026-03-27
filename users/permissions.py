from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверка: пользователь — модератор"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()


class IsNotModerator(BasePermission):
    """Проверка: пользователь — не модератор"""

    def has_permission(self, request, view):
        return not request.user.groups.filter(name="Moderators").exists()


class IsOwner(BasePermission):
    """Проверка: пользователь — создатель объекта"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user
