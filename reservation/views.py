import datetime
from os.path import exists

from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from user.permissions import wrap_permission
from user.views import (
    get_all_groups,
    return_forbiden,
    return_not_find,
    return_param_error,
    return_success,
)
from finance.serializers import PayRecordSerializer, PayItemSerializer
from finance.models import PayType

from .models import *
from .serializers import *


class ReservationTimeViewSet(viewsets.ModelViewSet):
    queryset = ReservationTime.objects.all()
    serializer_class = ReservationTimeSerializer

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @wrap_permission(permissions.IsAdminUser)
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

    @wrap_permission(permissions.IsAdminUser)
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
            return return_not_find("预约时间段不存在！")
        restime = restime[0]

        ser = ReservationTimeSerializer(
            instance=restime, data=data, partial=True
        )
        if not ser.is_valid():
            return return_param_error()

        ser.save()
        return return_success("更新成功！")

    @wrap_permission(permissions.IsAdminUser)
    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @wrap_permission(permissions.AllowAny)
    def retrieve(self, request, *args, **kwargs):
        time = ReservationTime.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not time:
            return return_not_find("预约时间段不存在！")
        time = time[0]

        data = ReservationTimeSerializer(time).data
        reserved_num = Reservation.objects.all().filter(time_id=time.id).count()
        data["reserved_num"] = reserved_num
        return Response(data=data, status=status.HTTP_200_OK)

    @wrap_permission(permissions.AllowAny)
    def list(self, request, *args, **kwargs):
        times = ReservationTime.objects.all()
        ser = ReservationTimeSerializer(times, many=True)
        ress = Reservation.objects.all()
        data = []
        for d in ser.data:
            reserved_num = ress.filter(time_id=d.get("id")).count()
            d["reserved_num"] = reserved_num
            data.append(d)

        return Response(data=data, status=status.HTTP_200_OK)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @wrap_permission(permissions.IsAdminUser)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        res = Reservation.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not res:
            return return_not_find("预约不存在！")
        res = res[0]

        # 如果请求的用户不是该预约的病人、医生或者不是管理员时无权限
        if (
            not res.patient == request.user
            and not res.doctor == request.user
            and not request.user.is_staff
        ):
            return return_forbiden()

        if not res.pay_id:
            return return_not_find("缴费记录不存在！")

        data = ReservationSerializer(res).data
        pay = PayRecordSerializer(res.pay)
        pay_data = pay.data
        pay_data["items"] = PayItemSerializer(res.pay.items, many=True).data
        data["pay"] = pay_data
        return Response(data=data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        # 不是管理员时无权指定病人
        if not request.user.is_staff:
            data["patient"] = request.user.id
        # 是管理员时必须指定病人
        elif request.user.is_staff and not data.get("patient", None):
            return return_param_error()

        # 转换日期
        date = data.get("date", None)
        if not date:
            return return_param_error("日期必须填写！")
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        data["date"] = date

        # 验证预约时间段是否还可以预约
        time_id = data.get("time", None)
        if not time_id:
            return return_param_error()
        time = ReservationTime.objects.all().filter(id=time_id)
        if not time:
            return return_not_find("预约时间段不存在！")
        time = time[0]
        # 已经预约了的人数
        num = Reservation.objects.all().filter(time=time_id).count()
        if num >= time.patient_num:
            return return_param_error("超过最大预约人数，不可预约！")

        doctor_id = data.get("doctor", None)
        # 没有指定医生时，代表是普通预约
        if not doctor_id:
            data["is_expert"] = 0
        else:
            data["is_expert"] = 1
            # 得到指定的医生
            doctor = User.objects.all().filter(id=doctor_id)
            if not doctor:
                return return_not_find("医生不存在！")
            doctor = doctor[0]

            # 验证指定的医生是否为专家医生
            expert = Group.objects.get(name="专家医生")
            if expert not in doctor.groups.all():
                return return_param_error("只能指定专家医生！")

            # 验证专家是否出诊
            visit = Visit.objects.all().filter(
                Q(doctor_id=doctor_id)
                & Q(date=date)
                & Q(start__lte=time.start)
                & Q(end__gte=time.end)
            )

            if not visit:
                return return_param_error("专家在此时间不出诊！")

            visit = visit[0]

            # 验证专家是否还可预约
            num = (
                Reservation.objects.all()
                .filter(Q(is_expert=1) & Q(doctor_id=doctor_id))
                .count()
            )
            if num >= visit.patient_num:
                return return_param_error("超过最大预约人数，不可预约！")

            data["doctor"] = doctor.id

        # 验证是不是已经有过预约
        if (
            Reservation.objects.all()
            .filter(
                Q(patient_id=data.get("patient", 0))
                & Q(time_id=time_id)
                & Q(date=date)
            )
            .exists()
        ):
            return return_param_error("此时间段已经预约，不可重复预约！")

        # 验证科室是否可以预约
        department = Group.objects.all().filter(
            id=request.data.get("department", 0)
        )
        if not department:
            return return_param_error("必须指定科室！")
        department = department[0]

        ds = get_all_groups(department)
        able = Group.objects.get(name="可预约科室")
        if able not in ds:
            return return_param_error("科室不可预约！")

        data["is_cancel"] = 0
        data["is_paid"] = 0
        data["is_finish"] = 0
        ser = ReservationSerializer(data=data)
        if not ser.is_valid():
            return return_param_error()

        res = ser.save()

        # 创建缴费记录
        pte = PayType.objects.get(name="专家号费用")
        ptn = PayType.objects.get(name="普通号费用")

        data = {
            "creator": request.user.id,
            "patient": request.user.id,
            "pay_type": pte.id if doctor_id else ptn.id
        }

        ser = PayRecordSerializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
        record = ser.save()

        res.pay = record
        res.save()

        data = {
            "name": pte.name if doctor_id else ptn.name,
            "count": 1,
            "price": pte.price if doctor_id else ptn.price,
            "record": record.id
        }
        ser = PayItemSerializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
        item = ser.save()
        
        return return_success("预约成功！")

    def update(self, request, *args, **kwargs):
        res = Reservation.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not res:
            return return_not_find("预约不存在！")
        res = res[0]

        # 如果请求的用户不是该预约的病人、医生或者不是管理员时无权限
        if (
            not res.patient == request.user
            and not res.doctor == request.user
            and not request.user.is_staff
        ):
            return return_forbiden()

        data = request.data
        date = data.get("date", None)
        doctor_id = data.get("doctor", res.doctor_id)
        time_id = data.get("time", None)
        patient_id = data.get("patient", res.patient_id)
        department_id = data.get("department", res.department_id)
        is_cancel = data.get("is_cancel", None)

        # 取消预约
        if is_cancel:
            res.is_cancel = 1
            res.save()
            return return_success("取消预约成功！")

        if date:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            data["date"] = date
        # TODO: 其他字段检测
        return return_success("更新预约成功！")

    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        分为两种情况
        1. 管理员创建，此时需要传入doctor来指定医生
        2. 专家医生创建，此时可不传入doctor（传入也不使用）
        """
        data = request.data
        doctor_id = request.data.pop("doctor", None)
        date = data.get("date", None)
        start = data.get("start", None)
        end = data.get("end", None)

        if not all((date, start, end)):
            return return_param_error()

        # 管理员请求但没有传入doctor
        if not doctor_id and request.user.is_staff:
            return return_param_error()

        expert = Group.objects.get(name="专家医生")
        # 请求者不是专家医生、不是管理员时无权限
        if (
            expert not in request.user.groups.all()
            and not request.user.is_staff
        ):
            return return_forbiden()

        doctor = request.user
        # 请求者是管理员，doctor需要另外指定
        if request.user.is_staff:
            doctor = User.objects.filter(id=doctor_id)
            if not doctor:
                return return_not_find("专家医生未找到！")
            doctor = doctor[0]

            # 指定的doctor不是专家医生
            if expert not in doctor.groups.all():
                return return_param_error()

        # 转换时间
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        start = datetime.datetime.strptime(start, "%H:%M").time()
        end = datetime.datetime.strptime(end, "%H:%M").time()

        data["date"] = date
        data["start"] = start
        data["end"] = end
        data["doctor"] = doctor.id

        ser = VisitSerializer(data=data)
        if not ser.is_valid():
            return return_param_error()

        ser.save()
        return return_success("创建成功！")

    def update(self, request, *args, **kwargs):
        visit = Visit.objects.all().filter(id=self.kwargs.get("pk", 0))
        if not visit:
            return return_not_find("坐诊时间不存在！")
        visit = visit[0]

        # 不是坐诊时间相关医生、不是管理员时没有操作权限
        if request.user != visit.doctor and not request.user.is_staff:
            return return_forbiden()

        # 如果是专家医生，不允许指定医生
        if not request.user.is_staff:
            request.data.pop("doctor")

        data = request.data
        # 时期、时间转换
        date = data.get("date", None)
        if date:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            data["date"] = date

        start = data.get("start", None)
        if start:
            start = datetime.datetime.strptime(start, "%H:%M").time()
            data["start"] = start

        end = data.get("end", None)
        if end:
            end = datetime.datetime.strptime(end, "%H:%M").time()
            data["end"] = end

        ser = VisitSerializer(instance=visit, data=data, partial=True)
        if not ser.is_valid():
            return return_param_error()
        ser.save()
        return return_success("更新成功！")

    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        visit = Visit.objects.filter(id=self.kwargs.get("pk", 0))
        if not visit:
            return return_not_find("坐诊时间不存在！")
        visit = visit[0]
        if visit.doctor != request.user and not request.user.is_staff:
            return return_forbiden()
        return super().destroy(request, *args, **kwargs)
