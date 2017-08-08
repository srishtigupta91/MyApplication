from rest_framework import serializers

from promotions.models import Coupons


class PromoCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupons
        fields = ("promotional_code","start_date","end_date","coupon_limit","status","notes",)