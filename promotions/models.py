from django.db import models

# Create your models here.
from accounts.models import User
from django.utils.translation import ugettext_lazy as _
#
# from brands.models import Brands, Categories

class Deals(models.Model):
    # brand = models.ForeignKey(Brands, related_name="brand_name")
    # category = models.ForeignKey(Categories, related_name="categories")
    amount = models.IntegerField()
    discounted_price = models.IntegerField()
    offer = models.CharField(max_length=250)
    location = models.CharField(max_length=100)
    rating = models.IntegerField()
    created_by = models.ForeignKey(User)
    expires_in = models.DateTimeField(auto_created=True)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Deal")
        verbose_name_plural = _('Deals')
        app_label = _('promotions')


class Coupons(models.Model):

    UNIQUE = 'unique'
    MULTIPLE = 'multiple'

    LIMIT_CHOICES = (
        (UNIQUE, 'Unique'),
        (MULTIPLE, 'Multiple'),
    )

    ACTIVE = 'active'
    INACTIVE = 'inactive'

    STATUS = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )

    promotional_code = models.CharField(verbose_name=_("Promotional Code"), max_length=30, unique=True)
    coupon_limit = models.CharField(_("Promotion Code Limit"),max_length=25, choices=LIMIT_CHOICES)
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    # brand = models.ForeignKey(Brands, related_name="brand_name")
    # category = models.ForeignKey(Categories, related_name="categories")
    status = models.CharField(max_length=250, choices=STATUS, default=ACTIVE)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['start_date']
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")
        app_label = _('promotions')

    def __str__(self):
        return self.promotional_code