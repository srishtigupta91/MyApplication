from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from fcm.models import AbstractDevice

from accounts.models import User


class StaticNotification(models.Model):
    TYPE = (("news",_("News")),("event",_("Event")),("schooltrip",_("School Trip")))

    notification_type= models.CharField(choices=TYPE, max_length=20)
    recipient_email = models.ForeignKey(User, related_name='recipient')
    unread = models.BooleanField(default=True,blank=False)
    actor = models.ForeignKey(User,related_name='actor_user')
    verb = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-timestamp', )

    def __unicode__(self):
        return 'actor:%s verb:%s'%(self.actor,self.verb)


class MyDevice(AbstractDevice):
    user = models.ForeignKey(User, related_name='fcm_user')
