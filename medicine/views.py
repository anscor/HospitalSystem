from .models import *
from .serializers import *

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from user.permissions import wrap_permission
from user.views import (
    return_success,
    return_forbiden,
    return_not_find,
    return_param_error,
)


class MedicineTypeViewSet(viewsets.ModelViewSet):
    queryset = MedicineType.objects.all()
    serializer_class = MedicineTypeSerializer

    @wrap_permission(permissions.IsAuthenticated)
    def create(self, request, *args, **kwargs):
        request.data["creator"] = request.user.id
        return super().create(request, *args, **kwargs)

    @wrap_permission(permissions.IsAuthenticated)
    def update(self, request, *args, **kwargs):

        mt = MedicineType.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not mt:
            return return_not_find("药物类型不存在！")
        mt = mt[0]

        data = request.data
        data["modifier"] = request.user.id
        ser = MedicineTypeSerializer(instance=mt, data=data, partial=True)
        if not ser.is_valid():
            return return_param_error()
        
        ser.save()
        return return_success("更新药物类型成功！")

    @wrap_permission(permissions.IsAuthenticated)
    def partial_update(self, request, *args, **kwargs):
        return Response(data=[], status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)