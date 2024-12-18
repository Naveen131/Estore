from django.test import TestCase
from rest_framework.test import APIClient
from .models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name="Test Product", description="A test product", price=100.0, stock=10)

    def test_get_products(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        response = self.client.post('/products', {
            "name": "New Product",
            "description": "A new product",
            "price": 50.0,
            "stock": 20
        })
        self.assertEqual(response.status_code, 200)

    def test_order_insufficient_stock(self):
        response = self.client.post('/orders', {
            "products": [{self.product.id: 25}]
        })
        self.assertEqual(response.status_code, 400)
