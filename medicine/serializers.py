from .models import *

from rest_framework import serializers


class MedicineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineType
        fields = "__all__"
