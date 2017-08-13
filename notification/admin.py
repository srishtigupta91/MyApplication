from django.contrib import admin

# Register your models here.

from .models import StaticNotification, MyDevice


class StaticNotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_type',
                    'recipient_email',
                    'actor',
                    'timestamp',
                    'unread')

    ordering = ('unread','timestamp')

admin.site.register(StaticNotification,StaticNotificationAdmin)
