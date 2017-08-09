from django.db.models.signals import post_save
from notification.signals import notify
from promotions.models import Deals

def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='was saved')

post_save.connect(my_handler, sender=Deals)