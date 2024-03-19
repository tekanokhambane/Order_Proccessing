from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User, Admin, Staff, Customer
from accounts.serializers import (
    UserSerializer,
    AdminSerializer,
    StaffSerializer,
    CustomerSerializer,
)


class TestSerializers(APITestCase):
    def test_user_serializer(self):
        """
        A test case to check the functionality of the user serializer with specific user attributes.
        """
        user = User.objects.create_user(
            first_name="test",
            last_name="user",
            username="testuser",
            password="testpassword",
            email="pZy0h@example.com",
        )
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data["username"], "testuser")

    def test_admin_serializer(self):
        """
        Test the serialization of an admin object.
        """
        user = User.objects.create_superuser(
            first_name="test",
            last_name="user",
            username="testuser",
            password="testpassword",
            email="pZy0h@example.com",
        )
        admin = Admin.objects.get(user=user)
        serializer = AdminSerializer(admin)
        self.assertEqual(serializer.data["user"], user.id)

    def test_staff_serializer(self):
        """
        Test the staff serializer function by creating a test user, retrieving the staff object,
        serializing the staff object, and asserting that the serialized data contains the correct user ID.
        """
        user = User.objects.create_staff(
            first_name="test",
            last_name="user",
            username="testuser",
            password="testpassword",
            email="pZy0h@example.com",
        )
        staff = Staff.objects.get(user=user)
        serializer = StaffSerializer(staff)
        self.assertEqual(serializer.data["user"], user.id)

    def test_customer_serializer(self):
        """
        Test the CustomerSerializer by creating a test user, retrieving a customer object,
        serializing it, and checking if the serialized data contains the correct user id.
        """
        user = User.objects.create_user(
            first_name="test",
            last_name="user",
            username="testuser",
            password="testpassword",
            email="pZy0h@example.com",
        )
        customer = Customer.objects.get(user=user)
        serializer = CustomerSerializer(customer)
        self.assertEqual(serializer.data["user"], user.id)
