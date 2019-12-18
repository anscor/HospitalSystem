from .models import *
from .serializers import *

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.contrib.auth.models import User, Group

from laboratory.models import Laboratory
from outpatient.models import Prescription
from user.permissions import wrap_permission
from reservation.models import Reservation

from common.data_nested import get_data_nested
from common.return_template import (
    return_param_error,
    return_not_find,
    return_forbiden,
    return_success,
    return_not_allow,
)


class PayTypeViewSet(viewsets.ModelViewSet):
    queryset = PayType.objects.all()
    serializer_class = PayTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data["creator"] = request.user.id
        request.data.pop("modifier", None)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        ins = PayType.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not ins:
            return return_param_error("缴费类型不存在！")
        ins = ins[0]

        data = request.data
        data.pop("creator", None)
        data.pop("creator", None)

        data["modifier"] = request.user.id
        ser = PayTypeSerializer(instance=ins, data=data, partial=True)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()
        return return_success("修改成功！")

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(
        methods=["GET"],
        detail=True,
        url_name="pay-records",
        url_path="pay-records",
    )
    def get_pay_records(self, request, pk=None):
        if not pk:
            return return_param_error()

        ins = PayType.objects.all().filter(id=pk)
        if not ins:
            return return_not_find("缴费类型不存在！")
        ins = ins[0]

        data = []
        if hasattr(ins, "records"):
            records = ins.records.all().filter(
                Q(receive__isnull=False) & Q(refund__isnull=False)
            )
            for rec in records:
                data.append(
                    get_data_nested(
                        rec, PayRecordSerializer, PayItemSerializer, many=True
                    )
                )
        return Response(data=data, status=status.HTTP_200_OK)


class PayRecordViewSet(viewsets.ModelViewSet):
    queryset = PayRecord.objects.all()
    serializer_class = PayRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 只是创建，但并不缴费，缴费通过更新来实现
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
        # 默认为预约费用，此时的病人为请求者
        data["patient"] = request.user.id
        data["creator"] = request.user.id
        data["pay_type"] = pay_type_id

        # 更改patient
        obj = None
        if pay_type.name == "化验单费用":
            obj = Laboratory.objects.all().filter(id=re_id)
        elif pay_type.name == "处方签费用":
            obj = Prescription.objects.all().filter(id=re_id)
        else:
            obj = User.objects.all().filter(id=re_id)

        if not obj:
            return return_param_error()
        obj = obj[0]
        if not isinstance(obj, User):
            # 此单号已经缴费过了
            if obj.pay:
                return Response(
                    get_data_nested(
                        obj.pay,
                        PayRecordSerializer,
                        PayItemSerializer,
                        many=True,
                    )
                )
            data["patient"] = obj.patient_id
        else:
            pg = Group.objects.get(name="病人")
            if pg not in obj.groups.all():
                return return_param_error("此用户不是病人！")

            data["patient"] = re_id
        # 创建记录
        ser = PayRecordSerializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()
        record = ser.save()

        # 创建对应item
        if isinstance(obj, User):
            data = {
                "record": record.id,
                "name": pay_type.name,
                "count": 1,
                "price": pay_type.price,
            }
            ser = PayItemSerializer(data=data)
            if not ser.is_valid():
                print(ser.errors)
                return return_param_error()
            ser.save()

            return Response(
                data=get_data_nested(
                    record, PayRecordSerializer, PayItemSerializer, many=True
                ),
                status=status.HTTP_201_CREATED,
            )
        else:
            # 如果对应处方、化验单没有对应的条目（不允许这种情况出现）
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
            # 如果是处方签
            else:
                for item in items:
                    d = {
                        "record": record.id,
                        "name": item.medicine.name,
                        "count": item.count,
                        "price": item.medicine.price * item.count,
                    }
                    data.append(d)

            ser = PayItemSerializer(data=data, many=True)
            if not ser.is_valid():
                print(ser.errors)
                return return_param_error()
            ser.save()
            obj.pay = record
            obj.save()
            return Response(
                data=get_data_nested(
                    record, PayRecordSerializer, PayItemSerializer, many=True
                ),
                status=status.HTTP_201_CREATED,
            )

    def update(self, request, *args, **kwargs):
        record = PayRecord.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not record:
            return return_not_find("缴费记录不存在！")
        record = record[0]

        receive = request.data.get("receive", None)
        refund = request.data.get("refund", None)
        method = request.data.get("method", None)

        if not all((receive, method)):
            return return_param_error()

        data = {
            "receive": receive,
            "method": method,
            "refund": refund if refund else 0,
        }

        ser = PayRecordSerializer(instance=record, data=data, partial=True)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()

        ser.save()
        if hasattr(record, "reservation"):
            record.reservation.is_paid = True
            record.reservation.save()
        return Response(
            data=get_data_nested(
                record, PayRecordSerializer, PayItemSerializer, many=True
            ),
            status=status.HTTP_200_OK,
        )

    def list(self, request, *args, **kwargs):
        records = PayRecord.objects.all().filter(
            Q(receive__isnull=False) & Q(refund__isnull=False)
        )

        data = []
        for record in records:
            d = get_data_nested(
                record,
                PayRecordSerializer,
                PayItemSerializer,
                "items",
                "items",
                True,
            )
            data.append(d)

        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        record = PayRecord.objects.all().filter(id=self.kwargs.get("pk", 0))
        record = record.filter(
            Q(receive__isnull=False) & Q(refund__isnull=False)
        )
        if not record:
            return return_not_find("缴费记录不存在！")
        record = record[0]

        data = get_data_nested(
            record,
            PayRecordSerializer,
            PayItemSerializer,
            "items",
            "items",
            True,
        )
        return Response(data=data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class RefundRecordViewSet(viewsets.ModelViewSet):
    queryset = RefundRecord.objects.all()
    serializer_class = RefundRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        return return_not_allow()

    def partial_update(self, request, *args, **kwargs):
        return return_not_allow()

    def create(self, request, *args, **kwargs):
        request.data["creator"] = request.user.id
        ser = RefundRecordSerializer(data=request.data)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()

        ins = ser.save()

        items = request.data.get("items", None)
        if not items:
            return return_param_error()

        for item in items:
            item["record"] = ins.id

        ser = RefundRecordItemSerializer(data=items, many=True)
        if not ser.is_valid():
            ins.delete()
            print(ser.errors)
            return return_param_error()
        ser.save()
        return return_success("退款记录创建成功！")

    def list(self, request, *args, **kwargs):
        records = RefundRecord.objects.all()
        data = []
        for record in records:
            data.append(
                get_data_nested(
                    record,
                    RefundRecordSerializer,
                    RefundRecordItemSerializer,
                    many=True,
                )
            )

        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        record = RefundRecord.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not record:
            return return_not_find()
        record = record[0]

        data = get_data_nested(
            record,
            RefundRecordSerializer,
            RefundRecordItemSerializer,
            many=True,
        )
        return Response(data=data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        pass


class AuditRecordViewSet(viewsets.ModelViewSet):
    queryset = AuditRecord.objects.all()
    serializer_class = AuditRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = {"applicant": request.user.id}
        ser = AuditRecordSerializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()
        ins = ser.save()

        items = request.data
        for item in items:
            item["audit"] = ins.id
        ser = AuditItemSerializer(data=items, many=True)
        if not ser.is_valid():
            ins.delete()
            print(ser.errors)
            return return_param_error()
        ser.save()
        return return_success("审核记录创建成功！")

    def list(self, request, *args, **kwargs):
        inss = AuditRecord.objects.all()
        data = []
        for ins in inss:
            data.append(
                get_data_nested(
                    ins, AuditRecordSerializer, AuditItemSerializer, many=True
                )
            )
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        ins = AuditRecord.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not ins:
            return return_not_find("审核记录不存在！")
        ins = ins[0]

        return Response(
            get_data_nested(
                ins, AuditRecordSerializer, AuditItemSerializer, many=True
            ),
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        return return_not_allow()

    def update(self, request, *args, **kwargs):
        ins = AuditRecord.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not ins:
            return return_not_find("审核记录不存在！")
        ins = ins[0]

        data = {
            "result": request.data.get("result", None),
            "commet": request.data.get("commet", None),
        }

        if data["result"]:
            data["result"] = 1
        data["auditor"] = request.user.id

        ser = AuditRecordSerializer(instance=ins, data=data, partial=True)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()
        ser.save()
        return return_success("审核记录修改成功！")

    def partial_update(self, request, *args, **kwargs):
        return return_not_allow()
