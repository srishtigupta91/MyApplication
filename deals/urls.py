from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from deals import views


router = DefaultRouter()
router.register('deals',views.DealsViewSets)

urlpatterns = [
    url(r'^', include(router.urls)),
]