from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product

from product.serializers import ProductSerializer


PRODUCTS_URL = reverse('product:product-list')


def detail_url(product_slug):
    """Return product detail URL"""
    return reverse('product:product-detail', args=[product_slug])


def sample_product(**params):
    """Create and return sample product"""
    defaults = {
        'name': 'TestNameCase',
        'description': "test description for test Product",
        'cost': 45
    }
    defaults.update(params)

    return Product.objects.create(**defaults)


class PublicProductsApiTests(TestCase):
    """Test the publicly available products API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(PRODUCTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductApiTests(TestCase):
    """Test products can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='TestMail@gmail.com',
            password='TestPassword123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_product_list(self):
        """Test retrieving list of products"""
        params = {
            'name': 'TestProduct',
            'description': 'Test description for second test product',
            'cost': 5.00
        }
        sample_product(**params)
        sample_product()
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        res = self.client.get(PRODUCTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_product_detail(self):
        """Test viewing product detail"""
        product = sample_product()
        url = detail_url(product.slug)
        res = self.client.get(url)

        serializer = ProductSerializer(product)
        self.assertEqual(serializer.data, res.data)
