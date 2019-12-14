from .models import *

from rest_framework import serializers

class ReservationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationTime
        fields = "__all__"
