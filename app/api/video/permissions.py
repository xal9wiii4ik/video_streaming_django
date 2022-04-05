import typing as tp

from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

from api.video.models import Video


class IsOwnerOrReadOnlyVideoPermission(BasePermission):
    """
    Permission for staff or teacher or view for all users
    """

    def has_permission(self, request: Request, view: tp.Any) -> bool:
        return bool(
            request.method in SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request: Request, view: tp.Any, obj: Video) -> bool:
        return bool(
            request.method in SAFE_METHODS or request.user == obj.account
        )
