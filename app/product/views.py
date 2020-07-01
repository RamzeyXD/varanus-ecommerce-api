from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from product import serializers
from core.models import Product


class ProductApiViewSet(viewsets.ReadOnlyModelViewSet):
    """Product endpoint to retrive list and single object"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'slug'
