from django.db import models
from django.utils.translation import ugettext_lazy as _

# # Create your models here.
from promotions.models import Deals, Coupons


class Brands(models.Model):

    PENDING = "pen"
    SUBMIT = "sub"
    APPROVE = "app"
    REJECT = "rej"
    PENALTY = "penality"

    STATUS = (
        (PENDING, _("Campaign Created")),
        (SUBMIT, _("Submit")),
        (APPROVE, _("Approved")),
        (REJECT, _("Rejected")),
        (PENALTY, _("Penalty")),
    )

    name = models.CharField(max_length=250)
    short_description = models.CharField(max_length=100)
    detailed_description = models.CharField(max_length=250)
    status = models.CharField(choices=STATUS, max_length=2)
    main_page_logo = models.ImageField(
        verbose_name=_("Logo Image of campaign"),
        upload_to='campaign/',
        blank=True,
        null=True
    )
    detail_page_logo = models.ImageField(
        verbose_name=_("Logo Image of campaign"),
        upload_to='campaign/',
        blank=True,
        null=True
    )
    created = models.DateField(auto_now_add=True)
    submitted = models.DateField(blank=True, null=True)
    approved = models.DateField(blank=True, null=True)
    approved_by = models.ForeignKey("accounts.User", blank=True, null=True)
    notifications = models.CharField(max_length=250)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")
        app_label = "brands"


class Categories(models.Model):

    name = models.CharField(max_length=250)
    deals = models.ForeignKey(Deals, related_name="deals")
    coupons = models.ForeignKey(Coupons, related_name="coupons")
    counts = models.IntegerField()
    parent = models.ForeignKey(
        'self',
        verbose_name=_("Parent"),
        null=True,
        blank=True,
        related_name="children"
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        app_label = _("brands")

