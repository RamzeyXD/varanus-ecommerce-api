from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from product import serializers
from core.models import Product, Order


class ProductApiViewSet(viewsets.ReadOnlyModelViewSet):
    """Product endpoint to retrive list and single object"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = 'slug'


class OrderApiView(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """Order endpoint to retrive, create and retrive list objects"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()

    serializers = {
        'list': serializers.OrderSerializer,
        'retrieve': serializers.OrderSerializer,
        'create': serializers.OrderCreateSerializer,
    }

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return Order.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Create a new order"""
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializers['list'])
