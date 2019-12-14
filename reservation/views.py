from .models import *
from .serializers import *

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from user.permissions import wrap_permission
from user.views import return_param_error, return_success, return_not_find

import datetime


class ReservationTimeViewSet(viewsets.ModelViewSet):
    queryset = ReservationTime.objects.all()
    serializer_class = ReservationTimeSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        data = request.data
        start = data.get("start", None)
        end = data.get("end", None)
        if not all((start, end)):
            return return_param_error()
        
        # 转换时间
        start = datetime.datetime.strptime(start, "%H:%M").time()
        end = datetime.datetime.strptime(end, "%H:%M").time()
        data["start"] = start
        data["end"] = end
        ser = ReservationTimeSerializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()
        ser.save()
        return return_success("预约时间段添加成功！")
    
    def update(self, request, *args, **kwargs):
        data = request.data
        # 转换时间
        start = data.get("start", None)
        end = data.get("end", None)
        if start:
            start = datetime.datetime.strptime(start, "%H:%M").time()
            data["start"] = start
        if end:
            end = datetime.datetime.strptime(end, "%H:%M").time()
            data["end"] = end
        
        # 预约时间实例
        restime = ReservationTime.objects.filter(id=self.kwargs.get("pk"))
        if not restime:
            return return_not_find()
        restime = restime[0]
        
        ser = ReservationTimeSerializer(instance=restime, data=data, partial=True)
        if not ser.is_valid():
            return return_param_error()
        
        ser.save()
        return return_success()

    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @wrap_permission(permissions.AllowAny)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @wrap_permission(permissions.AllowAny)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
