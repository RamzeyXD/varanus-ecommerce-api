from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Order, Product

from product.serializers import OrderSerializer


ORDERS_URL = reverse('product:order-list')


def sample_product(**params):
    """Create and return sample product"""
    defaults = {
        'name': 'TestNameCase',
        'description': "test description for test Product",
        'cost': 45
    }
    defaults.update(params)

    return Product.objects.create(**defaults)


def sample_order(user, *products):
    """Create and return sample order"""
    order = Order.objects.create(
        owner=user
    )
    order.products.add(*products)
    return order


class PublicOrderApiTests(TestCase):
    """Test the publicly available order API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(ORDERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderApiTests(TestCase):
    """Test orders can be retrieved and created by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='TestMailOrder@gmail.com',
            password='TestPassword123'
        )
        self.client.force_authenticate(self.user)

    def test_create_valid_order_success(self):
        """Test create order with valid payload is successful"""
        product = sample_product()
        payload = {'products': [product.id, ]}

        res = self.client.post(ORDERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(product.id, res.data['products'])

    def test_create_invalid_order(self):
        """Test create order with invalid payload"""
        payload = {'products': [158, ]}
        res = self.client.post(ORDERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_order_list(self):
        """Test retrieving list of orders"""
        params = {
            'name': 'SecondPr',
            'description': 'Second product description',
            'cost': 75
        }
        product_1 = sample_product()
        product_2 = sample_product(**params)

        sample_order(self.user)
        sample_order(self.user, product_1, product_2)

        res = self.client.get(ORDERS_URL)

        user_orders = Order.objects.filter(owner=self.user)
        serializer = OrderSerializer(user_orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_orders_limited_to_user(self):
        """Test that orders for authenticated user are returned"""
        user2 = get_user_model().objects.create(
            email='User2lgjh',
            username='sdfsdf',
            password='passwrodTest123'
        )
        product = sample_product()
        sample_order(user2, product)
        sample_order(self.user, product)

        res = self.client.get(ORDERS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
