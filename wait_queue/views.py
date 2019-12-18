from wait_queue.models import WaitQueue
from wait_queue.serializers import WaitQueueSerializer

from django.contrib.auth.models import Group, User
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation.models import Reservation
from finance.models import PayRecord
from user.serializers import UserSerializer
from user.permissions import wrap_permission

from common.return_template import return_param_error, return_success
from common.groups import get_all_groups

import datetime
import bisect


wait_queues = {"doctor": {}, "department": {}}


class WaitQueueViewSet(viewsets.ViewSet):

    queryset = WaitQueue.objects.all()
    serializer_class = WaitQueueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def _add_into_queue(self, instance):
        # 如果是专家号，则加入到相应的专家号排队队列中
        if instance.doctor:
            if instance.doctor.id not in wait_queues["doctor"].keys():
                wait_queues["doctor"][instance.doctor.id] = []
            if instance in wait_queues["doctor"][instance.doctor.id]:
                return False
            bisect.insort(wait_queues["doctor"][instance.doctor.id], instance)
        # 否则分科室进行排队
        else:
            if instance.department.id not in wait_queues["department"].keys():
                wait_queues["department"][instance.department.id] = []
            if instance in wait_queues["department"][instance.department.id]:
                return False
            bisect.insort(
                wait_queues["department"][instance.department.id], instance
            )

        return True

    def create(self, request, *args, **kwargs):
        data = request.data

        patient_id = data.get("patient", None)
        reservation_id = data.get("reservation", None)
        department_id = data.get("department", None)
        pay_id = data.get("pay", None)
        doctor_id = data.get("doctor", None)

        # 如果传入了预约，进行预约检查
        if reservation_id:
            reservation = Reservation.objects.all().filter(id=reservation_id)
            if not reservation:
                return return_param_error("预约不存在！")
            reservation = reservation[0]

            if reservation.is_cancel:
                return return_param_error("该预约已取消！")

            if reservation.date < datetime.datetime.today():
                return return_param_error("该预约已过期！")
            elif reservation.date > datetime.datetime.today():
                return return_param_error("该预约时间不是今天！")

            if reservation.time.end <= datetime.datetime.now().time():
                return return_param_error("该预约已过期！")

            if reservation.is_finish:
                return return_param_error("该预约已经使用过，无效！")

            if not reservation.is_paid or not reservation.pay:
                return return_param_error("该预约还未缴费！")

            data = {
                "patient": reservation.patient.id,
                "doctor": reservation.doctor.id
                if reservation.doctor
                else None,
                "department": reservation.department.id,
                "pay": reservation.pay.id,
                "reservation": reservation.id,
            }
            ser = WaitQueueSerializer(data=data)
            if not ser.is_valid():
                print(ser.errors)
                return return_param_error()

            ins = ser.save()
            if self._add_into_queue(ins):
                # 更新
                ins.reservation.is_finish = 1
                ins.reservation.save()
                return return_success("成功加入到排队队列中！")
            else:
                return return_param_error("已经在排队中，不能重复添加！")

        # 不是预约，现场挂号病人排队
        # 进行各项参数检查
        if not all((patient_id, department_id, pay_id)):
            return return_param_error()

        patient = User.objects.all().filter(id=patient_id)
        if not patient:
            return return_param_error("病人不存在！")
        patient = patient[0]

        pg = Group.objects.get(name="病人")
        if pg not in patient.groups.all():
            return return_param_error("此用户不是病人！")

        department = Group.objects.all().filter(id=department_id)
        if not department:
            return return_param_error("科室不存在！")
        department = department[0]

        dg = Group.objects.get(name="科室")
        if dg not in get_all_groups(department):
            return return_param_error("组不是科室！")

        pay = PayRecord.objects.all().filter(id=pay_id)
        if not pay:
            return return_param_error("缴费记录不存在！")
        pay = pay[0]

        if pay.patient.id != patient.id:
            return return_param_error("病人与缴费记录不对应！")

        data = {
            "patient": patient_id,
            "department": department_id,
            "pay": pay_id,
        }
        # 专家号再检查专家id
        if doctor_id:
            doctor = User.objects.all().filter(id=doctor_id)
            if not doctor:
                return return_param_error("医生不存在！")
            doctor = doctor[0]

            edg = Group.objects.get(name="专家医生")
            if edg not in doctor.groups.all():
                return return_param_error("用户不是专家医生！")

            data["doctor"] = doctor_id

        ser = WaitQueueSerializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()
        if self._add_into_queue(ser.save()):
            return return_success("成功加入到排队队列中！")
        else:
            return return_param_error("已经在排队中，不能重复添加！")

    def list(self, request, *args, **kwargs):
        pg = Group.objects.get(name="病人")
        edg = Group.objects.get(name="专家医生")
        ndg = Group.objects.get(name="医生")
        dg = Group.objects.get(name="科室")

        doctor_id = request.query_params.get("doctor", None)
        department_id = request.query_params.get("department", None)
        top = request.query_params.get("top", None)

        if top and top != 1:
            return return_param_error("top指定1！")

        if all((doctor_id, department_id)):
            return return_param_error("医生与科室不能同时指定！")
        
        if top and not doctor_id and not department_id:
            return return_param_error("指定top时必须指定doctor或department！")

        data = {}
        if doctor_id:
            doctor = User.objects.all().filter(id=doctor_id)
            if not doctor:
                return return_param_error("医生不存在！")
            doctor = doctor[0]

            if edg not in doctor.groups.all():
                return return_param_error("必须指定专家医生！")

            data["doctor"] = {doctor_id: []}
            if doctor_id in wait_queues["doctor"].keys():
                for p in wait_queues["doctor"][doctor_id]:
                    if top:
                        data = UserSerializer(p.patient).data
                        data["doctor"][doctor_id].pop(0)
                        break
                    data["doctor"][doctor_id].append(
                        UserSerializer(p.patient).data
                    )

        if department_id:
            department = Group.objects.all().filter(id=department_id)
            if not department:
                return return_param_error("科室不存在！")
            department = department[0]

            if dg not in get_all_groups(department):
                return return_param_error("必须指定科室！")

            data["department"] = {department_id: []}
            if department_id in wait_queues["department"].keys():
                for p in wait_queues["department"][department_id]:
                    if top:
                        data = UserSerializer(p.patient).data
                        data["department"][department_id].pop(0)
                        break
                    data["department"][department_id].append(
                        UserSerializer(p.patient).data
                    )
        
        return Response(data=data, status=status.HTTP_200_OK)
