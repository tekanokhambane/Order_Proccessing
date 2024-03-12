from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from products.models import Product, ProductType
from products.serializers import ProductSerializer, ProductTypeSerializer
from accounts.models import User


class TestProductSerializer(APITestCase):
    def setUp(self):
        self.client = APIClient()
        image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )

        self.user = User.objects.create_staff(
            first_name="test",
            last_name="user",
            username="testuser",
            password="testpassword",
            email="pZy0h@example.com",
        )
        self.product_type = ProductType.objects.create(
            name="Test Product Type", assigned_to=self.user
        )
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Product Description",
            image="test.png",
            product_type=self.product_type,
            price=10.00,
        )

    def test_product_serializer(self):
        image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )

        serializer = ProductSerializer(self.product)
        expected_data = {
            "name": "Test Product",
            "description": "Test Product Description",
            "image": image,
            "product_type": self.product.product_type.id,
            "price": "10.00",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_create_product(self):
        data = {
            "name": "Test Product",
            "description": "Test Product Description",
            "image": "/media/products/table.png",
            "product_type": self.product_type.id,
            "price": "10.00",
        }
        serializer = ProductSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.description, "Test Product Description")
        self.assertEqual(product.image, "/media/test.png")
        self.assertEqual(product.product_type, self.product_type)
        self.assertEqual(product.price, 10.00)

    def test_create_product_with_invalid_data(self):
        data = {
            "name": "Test Product",
            "description": "Test Product Description",
            "image": "/media/test.png",
            "product_type": self.product_type.id,
            "price": "10.00",
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.description, "Test Product Description")
        self.assertEqual(product.image, "/media/test.png")
        self.assertEqual(product.product_type, self.product_type)
        self.assertEqual(product.price, "10.00")

    def test_product_type_serializer(self):
        serializer = ProductTypeSerializer(self.product_type)
        expected_data = {
            "name": "Test Product Type",
            "assigned_to": self.user.id,
            "action": "approve",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_product_type_serializer_with_action(self):
        self.product_type.action = "inspect"
        serializer = ProductTypeSerializer(self.product_type)
        expected_data = {
            "name": "Test Product Type",
            "assigned_to": self.user.id,
            "action": "inspect",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_create_product_type(self):
        data = {
            "name": "Test Product Type",
            "assigned_to": self.user.id,
            "action": "approve",
        }
        serializer = ProductTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        product_type = ProductType.objects.get(name="Test Product Type")
        self.assertEqual(product_type.assigned_to, self.user)
        self.assertEqual(product_type.action, "approve")
