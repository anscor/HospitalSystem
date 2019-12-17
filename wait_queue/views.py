from wait_queue.models import WaitQueue
from wait_queue.serializers import WaitQueueSerializer

from django.contrib.auth.models import Group, User
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from reservation.models import Reservation

from common.return_template import return_param_error, return_success

from queue import PriorityQueue
import datetime


wait_queue = PriorityQueue()


class WaitQueueViewSet(viewsets.ModelViewSet):
    queryset = WaitQueue.objects.all()
    serializer_class = WaitQueueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        data = request.data
        ser = WaitQueueSerializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
            return return_param_error()

        patient_id = data["patient"]
        reservation_id = data.get("reservation", None)

        patient = User.objects.all().filter(id=patient_id)
        if not patient:
            return return_param_error("病人不存在！")
        patient = patient[0]

        pg = Group.objects.get(name="病人")
        if pg not in patient.groups.all():
            return return_param_error("请求id不是病人！")
        
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

            if patient.id != reservation.patient_id:
                return return_param_error("该预约与该病人不对应！")
            
            if not reservation.is_paid:
                return return_param_error("该预约还未缴费！")
        
        ins = ser.save()

        # 加入排队
        wait_queue.put(ins)
        # 如果是预约，则修改预约已经使用
        if reservation_id:
            ins.reservation.is_finish = 1
            ins.reservation.save()

        return return_success("成功加入到排队队列中！")

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)