from django.db import models

from promotions.models import Deals, Coupons


class Categories(models.Model):

    name = models.CharField(max_length=250)
    deals = models.ForeignKey(Deals, related_name="deals")
    coupons = models.ForeignKey(Coupons, related_name="coupons")
    counts = models.IntegerField()
    parent = models.ForeignKey(
        'self',
        verbose_name="Parent",
        null=True,
        blank=True,
        related_name="children"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        app_label = "brands"
