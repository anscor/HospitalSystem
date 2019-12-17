from wait_queue.models import WaitQueue

from rest_framework import serializers

class WaitQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitQueue
        exclude = ["joined_time"]
