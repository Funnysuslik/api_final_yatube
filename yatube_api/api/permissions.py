from rest_framework import permissions


class IsAuthenticatedAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, основное на сверке пользователя
     и сверки автора запрашиваемого объекта
    """

    message = "Do not touch what is not yours"

    def has_object_permission(self, request, view, obj):

        return (
            (request.method in permissions.SAFE_METHODS)
            or obj.author == request.user
        )

    def has_permission(self, request, view):

        return (
            (request.method in permissions.SAFE_METHODS)
            or request.user.is_authenticated
        )
