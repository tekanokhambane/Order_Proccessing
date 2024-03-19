from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from products.views import ProductViewSet
from products.models import Product, ProductType


class TestProductViewSet(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = ProductViewSet.as_view({"get": "list"})
        self.client = APIClient()

    def test_get_with_products(self):
        """
        Test the GET request with products, including user authentication, and validate the response status code and data.
        """
        self.client.force_login(
            user=get_user_model().objects.create_user(
                username="test_user",
                email="test_userwkn@example.com",
                password="test_password",
                first_name="Test",
                last_name="User",
            )
        )

        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
