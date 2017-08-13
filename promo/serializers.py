from django.utils import timezone
from rest_framework import exceptions
from rest_framework import serializers

from .models import VoucherCode, BarCodes


class PromoCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VoucherCode
        fields = ('code', 'email_address',)

    def validate_code(self, code):
       if BarCodes.objects.filter(code=code, valid_from__lte=timezone.now(), valid_till__gte=timezone.now()).exists():
           return code
       raise exceptions.ValidationError("Voucher does not exists")
