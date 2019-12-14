from .models import *
from .serializers import *

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView

from user.permissions import wrap_permission


class logout(APIView):
    def get(self, request, *args, **kwargs):
        return Response(data={"detail": "成功登出！"}, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def _checkIsOwnerOrAdminUser(self, user_set, request):
        # 用户不存在
        if not user_set:
            return (
                Response(
                    data={"detail": "用户不存在！"},
                    status=status.HTTP_400_BAD_REQUEST,
                ),
                None,
            )

        # 不是本人也不是管理员
        user = user_set[0]
        if user != request.user and not request.user.is_staff:
            return (
                Response(
                    data={"detail": "无权限访问！"}, status=status.HTTP_403_FORBIDDEN
                ),
                None,
            )

        return user, True

    @wrap_permission(permissions.AllowAny)
    def create(self, request, *args, **kwargs):
        data = request.data.pop("profile", None)

        user_ser = UserSerializer(data=request.data)
        if not user_ser.is_valid():
            return Response(
                data={"detail": "参数错误！"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 用户名重复
        user = User.objects.all().filter(username=request.data.get("username"))
        if user:
            return Response(
                data={"detail": "用户已存在！"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = user_ser.save()

        # 如果没有传profile则直接返回
        if not data:
            return Response(
                data={"detail": "注册成功！"}, status=status.HTTP_200_OK
            )
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
            return Response(
                data={"detail": "注册成功！"}, status=status.HTTP_200_OK
            )
        else:
            # 如果profile创建失败，将原来已经添加的用户删除
            user.delete()
            return Response(
                data={"detail": "参数错误！"}, status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.all().filter(id=self.kwargs.get("pk", ""))

        ret, success = self._checkIsOwnerOrAdminUser(user, request)
        if not success:
            return ret

        ser = UserSerializer(ret)
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

        # 更新profile
        if profile_data and profile:
            profile_data["modifier"] = request.user.id
            ser = UserProfileSerializer(instance=profile, data=profile_data, partial=True)
            # 请求数据出错
            if not ser.is_valid() or not user_ser.is_valid():
                print(ser.errors)
                return Response(
                    data={"detail": "请求数据错误！"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ser.save()
            user_ser.save()
        # 删除profile
        elif not profile_data and profile:
            if not user_ser.is_valid():
                return Response(
                    data={"detail": "请求数据错误！"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            profile.delete()
            user_ser.save()
        # 创建profile
        elif not profile and profile_data:
            profile_data["user"] = ret.id
            profile_data["creator"] = request.user.id
            ser = UserProfileSerializer(data=profile_data)
            # 请求数据出错
            if not ser.is_valid() or not user_ser.is_valid():
                return Response(
                    data={"detail": "请求数据错误！"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ser.save()
            user_ser.save()
        else:
            if not user_ser.is_valid():
                return Response(
                    data={"detail": "请求数据错误！"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user_ser.save()

        return Response(
            data={"detail": "更改用户信息成功！"}, status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        pass

    @wrap_permission(permissions.IsAdminUser)
    def destroy(self, request, *args, **kwargs):
        user = User.objects.all().filter(id=self.kwargs.get("pk", ""))
        if user:
            user = user[0]
            profile = user.profile
            user.delete()
            if profile:
                profile.delete()
            return Response(
                data={"detail": "成功删除用户！"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={"detail": "用户不存在！"}, status=status.HTTP_400_BAD_REQUEST
            )
