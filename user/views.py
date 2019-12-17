from .models import *
from .serializers import *

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView

from common.return_template import (
    return_forbiden,
    return_not_find,
    return_param_error,
    return_success,
    return_create,
)
from common.groups import get_all_groups
from common.data_nested import get_data_nested

from user.permissions import wrap_permission
from reservation.serializers import VisitSerializer, ReservationSerializer
from reservation.models import Reservation
from outpatient.serializers import (
    PrescriptionSerializer,
    PrescriptionItemSerializer,
    MedicalRecordSerializer,
)
from laboratory.serializers import (
    LaboratoryItemSerializer,
    LaboratorySerializer,
)


class UserLogout(APIView):
    def get(self, request, *args, **kwargs):
        return return_success("成功登出！")


class UserGet(APIView):
    @wrap_permission(permissions.IsAuthenticated)
    def get(self, request, *args, **kwargs):
        ser = UserSerializer(request.user)
        return Response(data=ser.data, status=status.HTTP_200_OK)


class Department(APIView):
    def get(self, request, *args, **kwargs):
        group = Group.objects.all().filter(name="可预约科室")
        if not group:
            return Response(data="", status=status.HTTP_200_OK)
        group = group[0]
        if not hasattr(group, "children_groups"):
            return Response(data="", status=status.HTTP_200_OK)

        gs = group.children_groups.all()
        groups = [g.group for g in gs]
        ser = GroupSerializer(groups, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def list(self, request, *args, **kwargs):
        name = request.query_params.get("name", None)
        groups = Group.objects.all()
        if name:
            groups = groups.filter(name=name)
        if not groups:
            return return_not_find("没有相应的组！")
        ser = GroupSerializer(groups, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)

    @wrap_permission(permissions.IsAdminUser)
    def create(self, request, *args, **kwargs):
        profile_data = request.data.pop("profile", None)
        ser = GroupSerializer(data=request.data)
        if not ser.is_valid():
            return return_param_error()

        group = ser.save()

        # 没有profile直接返回
        if not profile_data:
            return return_create(ser.data)

        profile_data["creator"] = request.user.id
        profile_data["group"] = group.id
        ser = GroupProfileSerializer(data=profile_data)
        if not ser.is_valid():
            group.delete()
            return return_param_error()

        ser.save()
        return return_create(GroupSerializer(group).data)

    @wrap_permission(permissions.IsAdminUser)
    def update(self, request, *args, **kwargs):
        profile_data = request.data.pop("profile", None)
        group = Group.objects.filter(id=self.kwargs.get("pk"))
        if not group:
            return return_not_find("用户组不存在！")

        group = group[0]
        group_ser = GroupSerializer(
            instance=group, data=request.data, partial=True
        )
        if not group_ser.is_valid():
            return return_param_error()

        profile = group.profile

        # 更新profile
        if profile_data and profile:
            profile_data["modifier"] = request.user.id
            profile_ser = GroupProfileSerializer(
                instance=profile, data=profile_data, partial=True
            )
            if not profile_ser.is_valid():
                return return_param_error()
            profile_ser.save()
        # 创建profile
        elif not profile and profile_data:
            profile_data["group"] = group.id
            profile_data["creator"] = request.user.id
            profile_ser = GroupProfileSerializer(data=profile_data)
            if not profile_ser.is_valid():
                return return_param_error()
            profile_ser.save()

        group_ser.save()
        return return_success("修改成功！")

    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        group = Group.objects.filter(id=self.kwargs.get("pk", 0))
        if not group:
            return return_not_find("用户组不存在！")
        group = group[0]
        profile = group.profile
        if profile:
            profile.delete()

        group.delete()
        return return_success("成功删除用户组！")

    def get_group_users(self, request, pk=None):
        if not pk:
            return return_param_error()

        group = Group.objects.filter(id=pk)
        if not group:
            return return_not_find("用户组不存在！")
        group = group[0]

        ser = UserSerializer(group.user_set.all(), many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)

    def add_group_users(self, request, pk=None):
        if not pk:
            return return_param_error()

        group = Group.objects.filter(id=pk)
        if not group:
            return return_not_find("用户组不存在！")
        group = group[0]

        user_id = request.data.get("user", None)
        if not user_id:
            return return_param_error()

        user = User.objects.filter(id=user_id)
        if not user:
            return return_not_find("用户不存在！")

        user = user[0]
        if user in group.user_set.all():
            return return_param_error("用户已在所添加的组内！")

        group.user_set.add(user)
        return return_success("添加成功！")

    @wrap_permission(permissions.IsAuthenticated)
    @action(
        methods=["POST", "GET"],
        detail=True,
        url_name="users",
        url_path="users",
    )
    def group_users(self, request, pk=None):
        if request.method == "POST":
            return self.add_group_users(request, pk)
        else:
            return self.get_group_users(request, pk)

    @wrap_permission(permissions.IsAuthenticated)
    @action(
        methods=["GET"],
        detail=True,
        url_name="reservations",
        url_path="reservations",
    )
    def get_reservations(self, request, pk=None):
        if not pk:
            return return_param_error()

        group = Group.objects.filter(id=pk)
        if not group:
            return return_not_find("用户组不存在！")
        group = group[0]

        if not hasattr(group, "reservations"):
            return Response(data=[], status=status.HTTP_200_OK)

        ser = ReservationSerializer(group.reservations.all(), many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def _checkIsOwnerOrAdminUser(self, user_set, request):
        # 用户不存在
        if not user_set:
            return return_not_find("用户不存在！"), None

        # 不是本人也不是管理员
        user = user_set[0]
        if user != request.user and not request.user.is_staff:
            return return_forbiden(), None

        return user, True

    @wrap_permission(permissions.AllowAny)
    def create(self, request, *args, **kwargs):
        data = request.data.pop("profile", None)
        group_id = request.data.pop("group", None)

        # 用户名重复
        user = User.objects.all().filter(username=request.data.get("username"))
        if user:
            return return_param_error("用户已存在！")

        # 用户组别，不传时默认为病人
        group = Group.objects.all().filter(name="病人")
        if group_id:
            group = Group.objects.all().filter(id=group_id)
            if not group:
                return return_not_find("用户组不存在！")

        group = group[0]

        user_ser = UserSerializer(data=request.data)
        if not user_ser.is_valid():
            return return_param_error()

        user = user_ser.save()

        # 如果没有传profile则直接返回
        if not data:
            return return_success("注册成功！")
        # 创建对应profile
        data["user"] = user.id
        data["creator"] = (
            request.user.id
            if not isinstance(request.user, AnonymousUser)
            else user.id
        )
        ser = UserProfileSerializer(data=data)
        # 创建成功
        if ser.is_valid():
            ser.save()
            gs = get_all_groups(group)
            for g in gs:
                user.groups.add(g)
            return return_success("注册成功！")
        else:
            # 如果profile创建失败，将原来已经添加的用户删除
            user.delete()
            return return_param_error()

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.all().filter(id=self.kwargs.get("pk", 0))

        if not user:
            return return_not_find("用户不存在！")
        user = user[0]

        # 如果请求者是病人，则不能查看别人的信息
        g = Group.objects.get(name="病人")
        if g in request.user.groups.all() and user != request.user:
            return return_forbiden()

        ser = UserSerializer(user)
        return Response(ser.data, status=status.HTTP_200_OK)

    @wrap_permission(permissions.IsAdminUser)
    def list(self, request, *args, **kwargs):
        users = User.objects.all()
        ser = UserSerializer(users, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = User.objects.all().filter(id=self.kwargs.get("pk", ""))

        ret, success = self._checkIsOwnerOrAdminUser(user, request)
        if not success:
            return ret

        profile = ret.profile
        profile_data = request.data.pop("profile", None)

        data = request.data
        data["username"] = ret.username
        user_ser = UserSerializer(instance=ret, data=request.data, partial=True)

        if not user_ser.is_valid():
            return return_param_error()

        # 更新profile
        if profile_data and profile:
            profile_data["modifier"] = request.user.id
            ser = UserProfileSerializer(
                instance=profile, data=profile_data, partial=True
            )
            # 请求数据出错
            if not ser.is_valid():
                return return_param_error()
            ser.save()
        # 创建profile
        elif not profile and profile_data:
            profile_data["user"] = ret.id
            profile_data["creator"] = request.user.id
            ser = UserProfileSerializer(data=profile_data)
            # 请求数据出错
            if not ser.is_valid():
                return return_param_error()
            ser.save()
        user_ser.save()

        return return_success("更改用户信息成功！")

    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        user = User.objects.all().filter(id=self.kwargs.get("pk", ""))

        if not user:
            return return_not_find("用户不存在！")

        user = user[0]
        profile = user.profile
        if profile:
            profile.delete()

        user.delete()
        return return_success("成功删除用户！")

    def get_user_groups(self, request, pk=None):
        if not pk:
            return return_param_error()
        user = User.objects.all().filter(id=pk)
        if not user:
            return return_not_find("用户不存在！")

        ret, success = self._checkIsOwnerOrAdminUser(user, request)
        if not success:
            return ret
        user = ret
        groups = user.groups.all()
        ser = GroupSerializer(groups, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)

    def add_user_groups(self, request, pk=None):
        if not pk:
            return return_param_error()

        if not request.user or not request.user.is_staff:
            return return_forbiden()

        user = User.objects.all().filter(id=pk)
        if not user:
            return return_not_find("用户不存在！")

        group_id = request.data.get("group", None)
        if not group_id:
            return return_param_error()

        group = Group.objects.all().filter(id=group_id)
        if not group:
            return return_not_find("用户组不存在！")

        group = group[0]
        user = user[0]
        user.groups.add(group)
        return return_success("添加成功！")

    @wrap_permission(permissions.IsAuthenticated)
    @action(
        methods=["GET", "POST"],
        detail=True,
        url_path="groups",
        url_name="groups",
    )
    def user_groups(self, request, pk=None):
        if request.method == "POST":
            return self.add_user_groups(request, pk)
        else:
            return self.get_user_groups(request, pk)

    @action(methods=["GET"], detail=True, url_name="visits", url_path="visits")
    def get_visit(self, request, pk=None):
        if not pk:
            return return_param_error()
        user = User.objects.filter(id=pk)
        if not user:
            return return_not_find("用户不存在！")
        user = user[0]

        expert = Group.objects.get(name="专家医生")
        # 对应用户不是专家医生，就不存在坐诊时间
        if expert not in user.groups.all():
            return return_param_error()

        ser = VisitSerializer(user.visits, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)

    @wrap_permission(permissions.IsAuthenticated)
    @action(
        methods=["GET"],
        detail=True,
        url_name="reservations",
        url_path="reservations",
    )
    def get_reservations(self, request, pk=None):
        if not pk:
            return return_param_error()
        user = User.objects.filter(id=pk)
        if not user:
            return return_not_find("用户不存在！")
        user = user[0]

        ress = Reservation.objects.all()
        pg = Group.objects.get(name="病人")
        expert = Group.objects.get(name="专家医生")
        # 如果请求都是病人
        if pg in request.user.groups.all():
            if user != request.user:
                return return_forbiden()
            ress = ress.filter(patient_id=user.id)
        # 请求者是对应的专家医生
        elif expert in request.user.groups.all():
            ress = ress.filter(doctor_id=request.user.id)
        # 并且请求都也不是管理员，无权限访问
        elif not request.user.is_staff:
            return return_forbiden()

        ser = ReservationSerializer(ress, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)

    @wrap_permission(permissions.IsAuthenticated)
    @action(
        methods=["GET"],
        detail=True,
        url_name="prescriptions",
        url_path="prescriptions",
    )
    def get_prescriptions(self, request, pk=None):
        if not pk:
            return return_param_error()
        user = User.objects.filter(id=pk)
        if not user:
            return return_not_find("用户不存在！")
        user = user[0]

        pg = Group.objects.get(name="病人")
        d = Group.objects.get(name="医生")

        data = []
        pres = None
        if pg in user.groups.all():
            if hasattr(user, "get_prescriptions"):
                pres = user.get_prescriptions.all()
        elif d in user.groups.all():
            if hasattr(user, "created_prescriptions"):
                pres = user.created_prescriptions.all()

        if pres:
            for pre in pres:
                d = PrescriptionSerializer(pre).data
                if hasattr(pre, "items"):
                    d["items"] = PrescriptionItemSerializer(
                        pre.items, many=True
                    ).data
                data.append(d)

        return Response(data=data, status=status.HTTP_200_OK)

    @wrap_permission(permissions.IsAuthenticated)
    @action(
        methods=["GET"],
        detail=True,
        url_path="medical-records",
        url_name="medical-records",
    )
    def get_medical_records(self, request, pk=None):
        if not pk:
            return return_param_error()
        user = User.objects.filter(id=pk)
        if not user:
            return return_not_find("用户不存在！")
        user = user[0]

        pg = Group.objects.get(name="病人")
        d = Group.objects.get(name="医生")

        data = []
        if pg in user.groups.all():
            if hasattr(user, "medical_records"):
                data = MedicalRecordSerializer(
                    user.medical_records, many=True
                ).data
        elif d in user.groups.all():
            if hasattr(user, "created_medical_records"):
                data = MedicalRecordSerializer(
                    user.created_medical_records, many=True
                ).data

        return Response(data=data, status=status.HTTP_200_OK)

    @wrap_permission(permissions.IsAuthenticated)
    @action(
        methods=["GET"],
        detail=True,
        url_path="laboratories",
        url_name="laboratories",
    )
    def get_laboratories(self, request, pk=None):
        if not pk:
            return return_param_error()
        user = User.objects.filter(id=pk)
        if not user:
            return return_not_find("用户不存在！")
        user = user[0]

        pg = Group.objects.get(name="病人")
        d = Group.objects.get(name="医生")

        data = []
        las = None
        if pg in user.groups.all():
            if hasattr(user, "laboratories"):
                las = user.laboratories.all()
        elif d in user.groups.all():
            if hasattr(user, "created_laboratories"):
                las = user.created_laboratories.all()

        if las:
            for la in las:
                d = LaboratorySerializer(la).data
                items = None
                if hasattr(la, "items"):
                    items = LaboratoryItemSerializer(la.items, many=True).data
                d["items"] = items
                data.append(d)

        return Response(data=data, status=status.HTTP_200_OK)


class OccupationViewSet(viewsets.ModelViewSet):
    queryset = Occupation.objects.all()
    serializer_class = OccupationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @wrap_permission(permissions.IsAdminUser)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @wrap_permission(permissions.IsAdminUser)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @wrap_permission(permissions.IsAdminUser)
    def partial_update(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @wrap_permission(permissions.IsAdminUser)
    @action(methods=["GET"], detail=True, url_path="users", url_name="users")
    def get_users(self, request, pk=None):
        if not pk:
            return return_param_error()

        occ = Occupation.objects.all().filter(id=pk)
        if not occ:
            return return_not_find("职业不存在！")

        occ = occ[0]
        users = User.objects.all().filter(profile__occupation=occ)
        ser = UserSerializer(users, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)


class BlackListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlackList.objects.all()
    serializer_class = BlackListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return Response(data="", status=status.HTTP_405_METHOD_NOT_ALLOWED)
