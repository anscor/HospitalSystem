from .models import *

from rest_framework import serializers


class PayTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayType
        fields = "__all__"


class PayItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayItem
        fields = "__all__"


class PayRecordSerializer(serializers.ModelSerializer):
    items = PayItemSerializer(required=False)

    class Meta:
        model = PayRecord
        fields = "__all__"
