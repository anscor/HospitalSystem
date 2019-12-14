from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
from functools import update_wrapper


def wrap_permission(*permissions, validate_permission=True):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            self.permission_classes = permissions
            if validate_permission:
                self.check_permissions(request)
            return func(self, request, *args, **kwargs)

        return update_wrapper(wrapper, func)

    return decorator