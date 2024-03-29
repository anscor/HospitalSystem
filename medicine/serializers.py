from .models import *

from rest_framework import serializers


class MedicineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineType
        fields = "__all__"


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"


class MedicineHandoutRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineHandoutRecord
        fields = "__all__"
