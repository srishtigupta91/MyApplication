import notifications.urls
from django.conf.urls import url, include

urlpatterns = [
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]