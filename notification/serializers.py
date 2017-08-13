import pytz
from rest_framework import serializers, views, viewsets, permissions, filters
from .models import StaticNotification
from accounts.models import User
from fcm.models import Device


class StaticNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaticNotification
        fields=('notification_type',)


from .models import MyDevice

class MyDeviceSerializer(serializers.Serializer):
    dev_id = serializers.CharField()
    reg_id = serializers.CharField()
    is_active = serializers.BooleanField(default=False)
    name = serializers.CharField(required=False)

    def validate(self, attrs):
        if MyDevice.objects.filter(dev_id=attrs['dev_id']).exists():
            MyDevice.objects.get(dev_id=attrs['dev_id']).delete()
        return attrs