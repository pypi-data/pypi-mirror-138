import logging

from django.conf import settings
from rest_framework.permissions import BasePermission


__all__ = ["BlockSchemaAccess"]


logger = logging.getLogger(__name__)


class BlockSchemaAccess(BasePermission):
    """Block schema access from OPTIONS request when not in DEBUG mode."""

    def has_permission(self, request, view):
        return not (request.method == "OPTIONS" and not settings.DEBUG)
