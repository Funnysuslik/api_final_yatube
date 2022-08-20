from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение, основное на сверке пользователя
     и сверки автора запрашиваемого объекта
    """

    message = "Do not touch what is not yours"

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:

            return True

        return obj.author == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Allows only to read if anonym."""

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:

            return True

        return request.user.is_authenticated
