from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """Проверяет, состоит ли пользователь в группе 'moderators'."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="moderators").exists()
        )


class IsOwner(BasePermission):
    """Разрешает доступ, если объект принадлежит пользователю."""

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "owner", None) == request.user
