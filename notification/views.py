from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import response
from rest_framework import generics, permissions, response, status, views, viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView


from fcm.models import Device
from fcm.serializers import DeviceSerializer
from accounts.models import User

import django_filters

from .serializers import *
from . models import StaticNotification


class NotificationView(ListAPIView):
    """
    method: GET
    url format: /api/v1/notifications/get/
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        notif=dict()
        recipient_obj = self.request.user

        notif['news_count'] = StaticNotification.objects.filter(recipient_email=recipient_obj,
                                                 unread=True, notification_type='news').count()

        notif['event_count'] = StaticNotification.objects.filter(recipient_email=recipient_obj,
                                                 unread=True, notification_type='event').count()

        notif['deals_count'] = StaticNotification.objects.filter(recipient_email=recipient_obj,
                                                     unread=True, notification_type='deals').count()

        return response.Response(notif, status=status.HTTP_200_OK)


class UpdateNotification(APIView):
    """
    method: POST
    url format: /api/v1/notifications/update/?type=news
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        notification_type = self.request.query_params['type']
        if notification_type == 'news':
            objs = StaticNotification.objects.filter(recipient_email=user, unread=True, notification_type='news')
            for obj in objs:
                # obj.unread=False
                obj.save()
        elif notification_type == 'event':
            objs = StaticNotification.objects.filter(recipient_email=user, unread=True, notification_type='event')
            for obj in objs:
                # obj.unread=False
                obj.save()
        elif notification_type == 'schooltrip':
            objs = StaticNotification.objects.filter(recipient_email=user, unread=True, notification_type='schooltrip')
            for obj in objs:
                # obj.unread=False
                obj.save()
        else:
            return response.Response({'message': 'incorrect type'}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response({'message':'notification for %s updated'%notification_type}, status=status.HTTP_200_OK)


from .models import MyDevice
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = MyDevice.objects.all()
    serializer_class = MyDeviceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print("create call")
        # return super(DeviceViewSet, self).create(request, *args, **kwargs)
        return response.Response(status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        user = self.request.user
        if MyDevice.objects.filter(user=user).exists():
            MyDevice.objects.filter(user=user).delete()
        serializer.validated_data['is_active']=True
        serializer.validated_data['user'] = user
        MyDevice.objects.create(**serializer.validated_data)
