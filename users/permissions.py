from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="Moderators").exists()
        )


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, "owner") and obj.owner == request.user


class IsModeratorOrOwner(BasePermission):
    """
    Доступ разрешен, если пользователь модератор или владелец объекта.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Moderators").exists():
            return True

        return hasattr(obj, "owner") and obj.owner == request.user
