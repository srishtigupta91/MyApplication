from rest_framework import serializers

from deals.models import Deals


class DealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deals
        fields = ('amount','discounted_price','offer','location','rating','created_by','expires_in')