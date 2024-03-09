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
        """
        Test the creation of a user by asserting the equality of user attributes.
        """
        self.assertEqual(self.user.email, "pZy0h@example.com")
        self.assertEqual(self.user.last_name, "last_name")
        self.assertEqual(self.user.first_name, "first_name")

    def test_user_creation_with_staff(self):
        """
        Test for creating a user with staff role, and asserting the created user's attributes.
        """
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
        """
        Test the creation of a user with superuser privileges.
        """
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
        """
        Test user creation with no email.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=None,
                last_name="last_name",
                first_name="first_name",
                password="password",
            )

    def test_user_creation_with_no_last_name(self):
        """
        Test user creation with no last name and expect IntegrityError from mysql database.
        """
        # raise mysql Integrity Error from mysql database
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="pZy5h@example.com",
                last_name=None,
                first_name="first_name",
                password="password",
            )

    def test_user_creation_with_no_first_name(self):
        """
        A test for user creation with no first name, ensuring that a mysql Integrity Error is raised from the mysql database.
        """
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
        """
        Test the creation of a staff member, checking various attributes for correctness.
        """
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
        """
        Test for creating an admin, checking various attributes of the created admin.
        """
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
        """
        Test for creating a customer, checking the user and its attributes.
        """
        customer = Customer.objects.get(user=self.user)
        self.assertEqual(customer.user, self.user)
        self.assertEqual(self.user.email, "pZy0h@example.com")
        self.assertEqual(self.user.last_name, "last_name")
        self.assertEqual(self.user.first_name, "first_name")

    def test_customer_billing_address(self):
        """
        Test the customer billing address by setting the billing address fields and saving the customer object. Then, assert that the billing address fields have been set correctly.
        """
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
