from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import NotificationView, UpdateNotification

from rest_framework import routers
from .views import DeviceViewSet

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^get/$', NotificationView.as_view()),
    url(r'^update/$', UpdateNotification.as_view()),
]