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
    class Meta:
        model = PayRecord
        fields = "__all__"


class RefundRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundRecord
        fields = "__all__"


class RefundRecordItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundRecordItem
        fields = "__all__"


class AuditRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditRecord
        fields = "__all__"


class AuditItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditItem
        fields = "__all__"
