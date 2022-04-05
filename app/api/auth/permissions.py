import typing as tp

from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

from django.contrib.auth import get_user_model


class IsOwnerOrReadOnlyAccountPermission(BasePermission):
    """
    Permission for owner or read only for user api
    """

    def has_permission(self, request: Request, view: tp.Any) -> bool:
        return bool(
            request.method in SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request: Request, view: tp.Any, obj: get_user_model) -> bool:
        return bool(
            request.method in SAFE_METHODS or request.user == obj
        )
