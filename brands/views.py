from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from accounts.permissions import IsAdvertiser, IsAdminOrAdvertiser
from .models.brands import *
from .models.categories import *
from .serializers import BrandSerializer, CategoriesSerializer


class BrandsView(viewsets.ModelViewSet):
    model = Brands
    serializer_class = BrandSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdvertiser,)
    queryset = Brands.objects.all()


class CategoriesView(viewsets.ModelViewSet):
    model = Categories
    serializer_class = CategoriesSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdminOrAdvertiser)
    queryset = Categories.objects.all()

