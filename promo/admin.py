from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from promo.models import Country,Store,VoucherCode,BarCodes, Config
from .actions import export_as_csv_action

admin.site.register(Country)
admin.site.register(Config)

class StoreAdmin(admin.ModelAdmin):
    list_display = ['name','country']

admin.site.register(Store,StoreAdmin)

class VoucherAdmin(admin.ModelAdmin):
    list_display = ['id','code', 'created','used']
    list_filter = (
        'used',
    )

    actions = [export_as_csv_action(
        "CSV Export",
        fields=[
            'id', 'code', 'store', 'first_name',
            'last_name','phone_number','email_address','used',
            'sex','age_gp'
        ],
    )]

    def get_queryset(self, request):
        return VoucherCode.objects.select_related('store').all()

admin.site.register(VoucherCode, VoucherAdmin)

class BarCodeAdmin(admin.ModelAdmin):
    list_display = ['id','bar_code','valid_from','valid_till','used']
    list_filter = (
        ('assign_date', DateFieldListFilter),
        'used'
    )
    fields = ('bar_code','valid_from','valid_till','used')

    actions = [export_as_csv_action(
        "CSV Export",
        fields=[
            'id', 'bar_code','valid_from','valid_till','used'
        ],
    )]

    def get_queryset(self, request):
        return BarCodes.objects.all()

admin.site.register(BarCodes,BarCodeAdmin)
