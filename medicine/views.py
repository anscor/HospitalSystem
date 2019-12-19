from .models import *
from .serializers import *

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from user.permissions import wrap_permission
from user.views import (
    return_success,
    return_forbiden,
    return_not_find,
    return_param_error,
)
from outpatient.serializers import (
    PrescriptionSerializer,
    PrescriptionItemSerializer,
)

from common.data_nested import get_data_nested


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

    @wrap_permission(permissions.IsAuthenticated)
    @action(
        methods=["GET"], detail=True, url_name="medicine", url_path="medicine"
    )
    def get_medicine(self, request, pk=None):
        if not pk:
            return return_param_error()

        t = MedicineType.objects.all().filter(id=pk)
        if not t:
            return return_not_find("药物类型不存在！")
        t = t[0]
        if not hasattr(t, "medicine"):
            return Response(data=[], status=status.HTTP_200_OK)
        ser = MedicineSerializer(t.medicine, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data["creator"] = request.user.id
        ser = MedicineSerializer(data=data)
        if not ser.is_valid():
            return return_param_error()
        ser.save()
        return return_success("创建药物成功！")

    def update(self, request, *args, **kwargs):
        m = Medicine.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not m:
            return return_not_find("药物不存在！")
        m = m[0]

        data = request.data
        data["modifier"] = request.user.id
        ser = MedicineSerializer(instance=m, data=data, partial=True)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()
        ser.save()
        return return_success("药物更新成功！")

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class MedicineHandoutRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicineHandoutRecord.objects.all()
    serializer_class = MedicineHandoutRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        mhrs = MedicineHandoutRecord.objects.all()
        data = []
        for mhr in mhrs:
            d = MedicineHandoutRecordSerializer(mhr).data
            d["prescription"] = get_data_nested(
                mhr.prescription,
                PrescriptionSerializer,
                PrescriptionItemSerializer,
                many=True,
            )
            data.append(d)
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        mhr = MedicineHandoutRecord.objects.all().filter(
            id=self.kwargs.get("pk", 0)
        )
        if not mhr:
            return return_not_find("药物发放记录不存在！")
        mhr = mhr[0]

        data = MedicineHandoutRecordSerializer(mhr).data
        data["prescription"] = get_data_nested(
            mhr.prescription,
            PrescriptionSerializer,
            PrescriptionItemSerializer,
            many=True,
        )
        return Response(data=data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mhr = MedicineHandoutRecord.objects.all().filter(
            id=self.kwargs.get("pk", 0)
        )
        if not mhr:
            return return_not_find("药物发放记录不存在！")
        mhr = mhr[0]

        # if mhr.handout_status:
        #     return return_param_error("药物已发放，不可更改！")

        data = {"handout_status": request.data.get("handout_status", None)}
        if not data["handout_status"]:
            return return_param_error()
        data["modifier"] = request.user.id
        ser = MedicineHandoutRecordSerializer(
            instance=mhr, data=data, partial=True
        )
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()
        mhr = ser.save()

        # 更改药物库存
        if mhr.handout_status == 4:
            for item in mhr.prescription.items.all():
                item.medicine.count -= item.count
                item.medicine.modifier = request.user
                item.medicine.save()

        data = MedicineHandoutRecordSerializer(mhr).data
        data["prescription"] = get_data_nested(
            mhr.prescription,
            PrescriptionSerializer,
            PrescriptionItemSerializer,
            many=True,
        )
        return Response(data=data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
