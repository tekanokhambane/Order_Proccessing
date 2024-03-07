from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from accounts.models import User, Admin, Staff, Customer

User = get_user_model()


class TestUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="pZy0h@example.com",
            last_name="last_name",
            first_name="first_name",
            password="password",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "pZy0h@example.com")
        self.assertEqual(self.user.last_name, "last_name")
        self.assertEqual(self.user.first_name, "first_name")

    def test_user_creation_with_staff(self):
        staff = User.objects.create_staff(
            email="pZy2h@example.com",
            last_name="last_name",
            first_name="first_name",
            password="password",
        )
        self.assertEqual(staff.email, "pZy2h@example.com")
        self.assertEqual(staff.last_name, "last_name")
        self.assertEqual(staff.first_name, "first_name")

    def test_user_creation_with_superuser(self):
        superuser = User.objects.create_superuser(
            email="pZy3h@example.com",
            last_name="last_name",
            first_name="first_name",
            password="password",
        )
        self.assertEqual(superuser.email, "pZy3h@example.com")
        self.assertEqual(superuser.last_name, "last_name")
        self.assertEqual(superuser.first_name, "first_name")

    def test_user_creation_with_no_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=None,
                last_name="last_name",
                first_name="first_name",
                password="password",
            )

    def test_user_creation_with_no_last_name(self):
        # raise mysql Integrity Error from mysql database
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="pZy5h@example.com",
                last_name=None,
                first_name="first_name",
                password="password",
            )

    def test_user_creation_with_no_first_name(self):
        # raise mysql Integrity Error from mysql database
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="pZy5h@example.com",
                last_name="last_name",
                first_name=None,
                password="password",
            )


class TestStaff(TestCase):
    def setUp(self):
        self.user = User.objects.create_staff(
            email="pZy2h@example.com",
            last_name="last_name",
            first_name="first_name",
            password="password",
        )

    def test_staff_creation(self):
        staff = Staff.objects.get(user=self.user)
        self.assertEqual(staff.user, self.user)
        self.assertEqual(self.user.email, "pZy2h@example.com")
        self.assertEqual(self.user.last_name, "last_name")
        self.assertEqual(self.user.first_name, "first_name")


class TestAdmin(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            email="pZy3h@example.com",
            last_name="last_name",
            first_name="first_name",
            password="password",
        )

    def test_admin_creation(self):
        admin = Admin.objects.get(user=self.user)
        self.assertEqual(admin.user, self.user)
        self.assertEqual(self.user.email, "pZy3h@example.com")
        self.assertEqual(self.user.last_name, "last_name")
        self.assertEqual(self.user.first_name, "first_name")


class TestCustomer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="pZy0h@example.com",
            last_name="last_name",
            first_name="first_name",
            password="password",
        )

    def test_customer_creation(self):
        customer = Customer.objects.get(user=self.user)
        self.assertEqual(customer.user, self.user)
        self.assertEqual(self.user.email, "pZy0h@example.com")
        self.assertEqual(self.user.last_name, "last_name")
        self.assertEqual(self.user.first_name, "first_name")

    def test_customer_billing_address(self):
        customer = Customer.objects.get(user=self.user)
        customer.billing_address_1 = "billing_address_1"
        customer.billing_address_2 = "billing_address_2"
        customer.billing_city = "billing_city"
        customer.billing_state = "billing_state"
        customer.billing_country = "billing_country"
        customer.save()

        self.assertEqual(customer.billing_address_1, "billing_address_1")
        self.assertEqual(customer.billing_address_2, "billing_address_2")
        self.assertEqual(customer.billing_city, "billing_city")
        self.assertEqual(customer.billing_state, "billing_state")
        self.assertEqual(customer.billing_country, "billing_country")
