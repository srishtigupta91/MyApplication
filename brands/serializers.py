from rest_framework import serializers

from .models.brands import Brands
from .models.categories import Categories


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brands
        fields = ("name","short_description","detailed_description","main_page_logo","detail_page_logo","status",)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name','parent','deals','coupons','counts',)