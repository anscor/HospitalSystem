from .models import *
from .serializers import *

from rest_framework import viewsets, permissions


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def partial_update(self, request, *args, **kwargs):
    #     user = request.user
    #     ser = UserSerializer(user, request.data, partial=True)
    #     if ser.is_valid():
    #         ser.save()
    #     return super().partial_update(request, *args, **kwargs)
