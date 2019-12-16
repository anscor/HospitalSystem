from .models import *
from .serializers import *

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from user.views import return_param_error, return_not_find, return_success

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
            "creator": request.user.id
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
