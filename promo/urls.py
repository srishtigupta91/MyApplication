from django.conf.urls import url,include
from .views import VoucherFormView, SendEmail

urlpatterns = [
    url(r'^$', VoucherFormView.as_view(),name="voucher-form"),
    url(r'^send/email/$', SendEmail),
]