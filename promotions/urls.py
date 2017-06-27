from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from promotions import views


router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
]