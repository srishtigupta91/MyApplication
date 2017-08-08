from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from brands import views


router = DefaultRouter()
router.register("brands", views.MakeBrandsView)
router.register('category',views.CategoriesView)

urlpatterns = [
    url(r'^', include(router.urls)),
]