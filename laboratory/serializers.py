from .models import *

from rest_framework import serializers


class LaboratoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryType
        fields = "__all__"


class LaboratoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryItem
        fields = "__all__"


class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = "__all__"
