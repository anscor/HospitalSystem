from .models import *

from rest_framework import serializers


class ReservationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationTime
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = "__all__"
