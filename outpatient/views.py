from .models import *
from .serializers import *

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from user.views import (
    return_param_error,
    return_not_find,
    return_success,
    get_all_groups,
)

import datetime


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # 验证是否传入patient和items
        patient_id = request.data.pop("patient", None)
        items = request.data.pop("items", None)
        if not patient_id or not items:
            return return_param_error()

        # 验证此id是否存在
        patient = User.objects.all().filter(id=patient_id)
        if not patient:
            return return_not_find("病人不存在！")
        patient = patient[0]

        # 验证此id对应用户是否为病人
        p = Group.objects.get(name="病人")
        if p not in patient.groups.all():
            return return_param_error("此用户不是病人！")

        # 创建处方签
        data = {
            "patient": patient_id,
            "is_paid": 0,
            "creator": request.user.id,
        }
        ser = PrescriptionSerializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()
        pre = ser.save()

        for item in items:
            item["prescription"] = pre.id

        ser = PrescriptionItemSerializer(data=items, many=True)
        if not ser.is_valid():
            pre.delete()
            print(ser.errors)
            return return_param_error()
        ser.save()
        return return_success("创建成功！")

    def list(self, request, *args, **kwargs):
        pres = Prescription.objects.all()
        data = []
        for pre in pres:
            d = PrescriptionSerializer(pre).data
            items = None
            if hasattr(pre, "items"):
                items = PrescriptionItemSerializer(pre.items, many=True).data
            d["items"] = items
            data.append(d)
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        pre = Prescription.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not pre:
            return return_not_find("处方签不存在！")
        pre = pre[0]
        data = PrescriptionSerializer(pre).data
        items = None

        if hasattr(pre, "items"):
            items = PrescriptionItemSerializer(pre.items, many=True).data

        data["items"] = items
        return Response(data=data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data

        onset_date = data.get("onset_date", None)
        patient_id = data.get("patient", None)
        department_id = data.get("department", None)

        if not all((onset_date, patient_id, department_id)):
            return return_param_error()

        data["onset_date"] = datetime.datetime.strptime(
            onset_date, "%Y-%m-%d"
        ).date()
        patient = User.objects.all().filter(id=patient_id)
        department = Group.objects.all().filter(id=department_id)

        if not patient or not department:
            print("xxx")
            return return_param_error()

        patient = patient[0]
        department = department[0]

        pg = Group.objects.get(name="病人")
        dg = Group.objects.get(name="科室")

        if pg not in patient.groups.all() or dg not in get_all_groups(
            department
        ):
            print("x")
            return return_param_error()

        data["time"] = datetime.datetime.now()
        data["can_modify"] = 1
        data["creator"] = request.user.id

        ser = MedicalRecordSerializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()
        ser.save()
        return return_success("创建成功！")

    def update(self, request, *args, **kwargs):
        record = MedicalRecord.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not record:
            return return_not_find("病历不存在！")
        record = record[0]

        if not record.can_modify:
            return return_param_error("此病历不可编辑！")

        data = request.data
        data["modifier"] = request.user.id
        onset_date = request.data.get("onset_date", None)
        if onset_date:
            data["onset_date"] = datetime.datetime.strptime(
                onset_date, "%Y-%m-%d"
            ).date()

        # 弹出不可更改的字段
        data.pop("id", None)
        data.pop("time", None)
        data.pop("create_time", None)
        data.pop("modify_time", None)
        data.pop("patient", None)
        data.pop("department", None)
        data.pop("creator", None)

        ser = MedicalRecordSerializer(instance=record, data=data, partial=True)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()

        ser.save()
        return return_success("修改成功！")

    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)
