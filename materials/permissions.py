from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsNotModeratorCreateDelete(BasePermission):
    """
    Модератор НЕ может:
    - POST
    - DELETE
    """

    def has_permission(self, request, view):
        if request.user.groups.filter(name="moderator").exists():
            return request.method not in ["POST", "DELETE"]
        return True


class IsOwner(BasePermission):
    """
    Разрешаем:
    - SAFE методы всем
    - изменение только владельцу
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user
