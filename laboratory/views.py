from django.shortcuts import render

from .serializers import *

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from user.permissions import wrap_permission

from common.return_template import (
    return_create,
    return_forbiden,
    return_not_find,
    return_param_error,
    return_success,
)
from common.data_nested import get_data_nested
from common.groups import get_all_groups


class LaboratoryTypeViewSet(viewsets.ModelViewSet):
    queryset = LaboratoryType.objects.all()
    serializer_class = LaboratoryTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @wrap_permission(permissions.IsAdminUser)
    def create(self, request, *args, **kwargs):
        request.data["creator"] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class LaboratoryViewSet(viewsets.ModelViewSet):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        las = Laboratory.objects.all()
        data = []

        for la in las:
            data.append(
                get_data_nested(
                    la,
                    LaboratorySerializer,
                    LaboratoryItemSerializer,
                    many=True,
                )
            )

        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        la = Laboratory.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not la:
            return return_not_find("化验单不存在！")
        la = la[0]

        data = get_data_nested(
            la, LaboratorySerializer, LaboratoryItemSerializer, many=True,
        )
        return Response(data=data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        pid = request.data.get("patient", None)
        eid = request.data.get("executor", None)
        items = request.data.get("items", None)

        if not all((pid, eid, items)):
            return return_param_error()

        p = User.objects.all().filter(id=pid)
        e = Group.objects.all().filter(id=eid)

        if not p or not e:
            return return_not_find("病人或执行科室不存在！")
        p = p[0]
        e = e[0]

        # 检查病人与科室对应的用户和组是否正确
        pg = Group.objects.get(name="病人")
        eg = Group.objects.get(name="科室")

        if pg not in p.groups.all() or eg not in get_all_groups(e):
            return return_param_error("病人id或科室id不正确！")

        data = {"patient": pid, "executor": eid, "creator": request.user.id}
        ser = LaboratorySerializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()
        la = ser.save()

        for item in items:
            item["laboratory"] = la.id

        ser = LaboratoryItemSerializer(data=items, many=True)
        if not ser.is_valid():
            la.delete()
            print(ser.errors)
            return return_param_error()
        ser.save()
        return return_success("创建成功！")

    def destroy(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)
