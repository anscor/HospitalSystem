from .models import *

from rest_framework import serializers


class PayTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayType
        fields = "__all__"
