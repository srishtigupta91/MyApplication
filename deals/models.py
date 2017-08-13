from django.db import models

# Create your models here.
from model_utils.managers import InheritanceManager

from accounts.models import User
from django.utils.translation import ugettext_lazy as _

from myapp import settings


class Deals(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="merchant_list")
    wallet_amount = models.DecimalField(decimal_places=2, max_digits=8)
    amount = models.IntegerField()
    discounted_price = models.IntegerField()
    offer = models.CharField(max_length=250)
    location = models.CharField(max_length=100)
    rating = models.IntegerField()
    created_by = models.ForeignKey(User)
    expires_in = models.DateTimeField(auto_created=True)
    created_on = models.DateTimeField(auto_now=True)
    objects = InheritanceManager()

    class Meta:
        verbose_name = "Deal"
        verbose_name_plural = 'Deals'
        app_label = 'deals'