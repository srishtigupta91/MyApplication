from rest_framework import permissions
from rest_framework import viewsets

from accounts.permissions import IsAdvertiser
from brands.models import Brands
from brands.serializers import BrandSerializer


class MakeBrandsView(viewsets.ModelViewSet):
    model = Brands
    serializer_class = BrandSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdvertiser,)
    queryset = Brands.objects.all()

