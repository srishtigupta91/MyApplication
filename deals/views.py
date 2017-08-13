from django.shortcuts import render

# Create your views here.
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from accounts.permissions import IsAdmin
from deals.models import Deals
from deals.serializers import DealSerializer

class DealsViewSets(viewsets.ModelViewSet):
    model = Deals
    queryset = Deals.objects.all()
    serializer_class = DealSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin,)