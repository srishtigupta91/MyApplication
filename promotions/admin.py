from django.contrib import admin

# Register your models here.
from promotions.models import Deals, Coupons

admin.site.register(Deals)
admin.site.register(Coupons)