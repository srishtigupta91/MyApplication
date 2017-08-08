from django.shortcuts import render

# Create your views here.
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from accounts.permissions import IsAdmin
from promotions.models import Coupons
from promotions.serializers import PromoCodeSerializer


class CouponsView(viewsets.ModelViewSet):
    model = Coupons
    queryset = Coupons.objects.all()
    serializer_class = PromoCodeSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('status',)