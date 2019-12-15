from .models import *
from .serializers import *

from rest_framework import viewsets, permissions

from user.permissions import wrap_permission


class PayTypeViewSet(viewsets.ModelViewSet):
    queryset = PayType.objects.all()
    serializer_class = PayTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data["creator"] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
