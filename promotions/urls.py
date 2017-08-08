from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from promotions import views


router = DefaultRouter()
router.register('coupons',views.CouponsView)

urlpatterns = [
    url(r'^', include(router.urls)),
]