from rest_framework.response import Response
from rest_framework import status


def return_param_error(msg="请求参数出错！"):
    return Response(data={"detail": msg}, status=status.HTTP_400_BAD_REQUEST)


def return_not_find(msg):
    return Response(data={"detail": msg}, status=status.HTTP_404_NOT_FOUND)


def return_forbiden(msg="无权限！"):
    return Response(data={"detail": msg}, status=status.HTTP_403_FORBIDDEN)


def return_success(msg):
    return Response(data={"detail": msg}, status=status.HTTP_200_OK)


def return_create(data):
    return Response(data=data, status=status.HTTP_201_CREATED)
