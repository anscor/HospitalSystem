from .models import *
from .serializers import *

from rest_framework import viewsets, permissions

from laboratory.models import Laboratory
from outpatient.models import Prescription
from user.permissions import wrap_permission
from user.views import (
    return_param_error,
    return_not_find,
    return_forbiden,
    return_success,
)


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


class PayRecordViewSet(viewsets.ModelViewSet):
    queryset = PayRecord.objects.all()
    serializer_class = PayRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        pay_type_id = request.data.get("type", None)
        re_id = request.data.get("id", None)

        if not all((pay_type_id, re_id)):
            return return_param_error()

        pay_type = PayType.objects.all().filter(id=pay_type_id)
        if not pay_type:
            return return_not_find("缴费类型不存在！")
        pay_type = pay_type[0]

        data = {}
        data["patient"] = request.user.id
        data["creator"] = request.user.id
        data["pay_type"] = pay_type_id

        # 更改patient
        obj = None
        if pay_type.name == "化验单费用":
            obj = Laboratory.objects.filter(id=re_id)
            if not obj:
                return return_param_error()
            obj = obj[0]
            data["patient"] = obj.patient_id
        elif pay_type.name == "处方签费用":
            obj = Prescription.objects.filter(id=re_id)
            if not obj:
                return return_param_error()
            obj = obj[0]
            data["patient"] = obj.patient_id

        # 创建记录
        ser = PayRecordSerializer(data=data)
        if not ser.is_valid():
            return return_param_error()
        record = ser.save()

        # 创建对应item
        # 没有obj则代表是预约费用
        if not obj:
            data = {
                "record": record.id,
                "name": pay_type.name,
                "count": 1,
                "price": pay_type.price,
            }
            ser = PayItemSerializer(data=data)
            if not ser.is_valid():
                return return_param_error()
            ser.save()
            return return_success("创建成功！")
        else:
            if not hasattr(obj, "items"):
                return return_param_error()

            data = []
            items = obj.items.all()
            # 如果是化验单
            if isinstance(obj, Laboratory):
                for item in items:
                    d = {
                        "record": record.id,
                        "name": item.laboratory_type.name,
                        "count": 1,
                        "price": item.laboratory_type.price,
                    }
                    data.append(d)
            else:
                for item in items:
                    d = {
                        "record": record.id,
                        "name": item.medicine.name,
                        "count": 1,
                        "price": item.medicine.price,
                    }
                    data.append(d)
            ser = PayItemSerializer(data=data, many=True)
            if not ser.is_valid():
                print(ser.errors)
                return return_param_error()
            ser.save()
            return return_success("创建成功！")

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
