from rest_framework import serializers

from brands.models import Brands


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brands
        fields = ("name","short_description", "detailed_description","main_page_logo","detail_page_logo","status",)
