from rest_framework import serializers

from core.models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product objects"""

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'cost')
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order objects"""
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'products')
        read_only_fields = ('id', )


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating order objects"""

    class Meta:
        model = Order
        fields = ('id', 'products')
        read_only_fields = ('id', )
