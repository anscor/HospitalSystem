from .models import *
from .serializers import *

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        data = request.data.pop("profile", None)

        # 参数没有传完
        if not username or not password:
            return Response(
                data={"detail": "username和password为必填字段！"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 用户名重复
        user = User.objects.all().filter(username=username)
        if user:
            return Response(
                data={"detail": "用户已存在！"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password)
        if email:
            user.email = email
            user.save()

        data["user"] = user.id
        data["creator"] = (
            request.user.id
            if not isinstance(request.user, AnonymousUser)
            else user.id
        )
        ser = UserProfileSerializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(data=[], status=status.HTTP_200_OK)
        else:
            user.delete()
            print(ser.errors)
            return Response(
                data={"detail": "参数错误！"}, status=status.HTTP_400_BAD_REQUEST,
            )

    @permission_classes([permissions.IsAuthenticated])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @permission_classes([permissions.IsAuthenticated])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_classes([permissions.IsAuthenticated])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_classes([permissions.IsAuthenticated])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @permission_classes([permissions.IsAdminUser])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
