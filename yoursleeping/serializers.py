from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Activity
        fields = ('date', 'time', 'heart_rate', 'type', 'sleep_time',)
