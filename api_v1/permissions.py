from rest_framework.permissions import SAFE_METHODS, BasePermission


class CreateUserPermission(BasePermission):
    """
    Неавторизованные пользователи могут создать объект User.

    Авторизованные могу запрашивать и обновлять информацию.
    """

    def has_permission(self, request, view):
        if view.action == "create" and not request.user.is_authenticated:
            return True
        return view.action != "create" and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj == request.user
            or request.method in SAFE_METHODS
        )
