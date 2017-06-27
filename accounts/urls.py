from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from accounts import views


router = DefaultRouter()
router.register("user", views.UserView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register/$', views.UserRegistration.as_view(), name="registration"),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(),name='logout'),
]