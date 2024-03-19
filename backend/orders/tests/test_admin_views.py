from django.test import TestCase
from unittest.mock import patch
from unittest import mock
from django.contrib.auth import get_user_model
from address.models import Address
from unittest.mock import Mock
from products.models import Product, ProductType
from orders.models import Order, OrderItem
from orders.admin import OrderAdmin

User = get_user_model()


@patch("orders.tasks.process_order.delay")
class TestOrderAdminSaveModel(TestCase):
    def setUp(self):
        """
        Set up the necessary objects for the test case.
        """
        self.user = User.objects.create_user(
            username="test_user",
            password="password",
            email="pZy0fkfh@example.com",
            first_name="Test",
            last_name="User",
        )
        self.admin_user = User.objects.create_superuser(
            username="admin_user",
            password="password",
            email="pZy0odidsh@example.com",
            first_name="Admin",
            last_name="User",
            is_staff=True,
        )
        self.address = Address.objects.create(
            line1="123 Main St",
            line2="Apt 1",
            city="Anytown",
            state="CA",
            zip_code="12345",
        )
        self.order_data = {
            "status": "created",
            "user": self.user,
            "shipping_address": self.address,
        }

    def test_save_model_calls_process_order(self, mock_process_order):
        """
        Test that the save_model method of the OrderAdmin class calls the process_order function with the correct arguments.

        :param mock_process_order: A mock object of the process_order function.
        :type mock_process_order: MagicMock

        :return: None
        :rtype: NoneType
        """

        admin = OrderAdmin(model=Order, admin_site=mock.Mock())
        order = Order.objects.create(**self.order_data)
        self.order_data["id"] = order.id
        self.order_data["amount"] = order.amount
        self.order_data["user"] = order.user.id
        admin.save_model(None, order, None, False)
        created_data = {
            "id": f"{order.id}",
            "status": f"{order.status}",
            "user": f"{order.user.id}",
            "shipping_address": f"{order.shipping_address.id}",
            "amount": f"{order.amount}",
        }

        mock_process_order.assert_called_once_with(created_data)


@patch("orders.tasks.process_order_item.delay")
class TestOrderAdminSaveRelated(TestCase):
    def setUp(self):
        """
        Set up initial data for testing including creating users, addresses, orders, product types, and products.
        """
        self.user = User.objects.create_user(
            username="test_user",
            password="password",
            email="pZy0poseh@example.com",
            first_name="Test",
            last_name="User",
        )
        self.admin_user = User.objects.create_superuser(
            username="admin_user",
            password="password",
            email="pZy098ekdh@example.com",
            first_name="Admin",
            last_name="User",
            is_staff=True,
        )
        self.address = Address.objects.create(
            line1="123 Main St",
            line2="Apt 1",
            city="Anytown",
            state="CA",
            zip_code="12345",
        )
        self.order = Order.objects.create(user=self.user, shipping_address=self.address)
        self.product_type = ProductType.objects.create(
            name="Test Product Type", action="inspect", assigned_to=self.admin_user
        )
        self.product = Product.objects.create(
            name="Test Product", price=10, product_type=self.product_type
        )

    def test_save_related_calls_process_order_item_create(
        self, mock_process_order_item
    ):
        """
        A test for the save_related method in the process_order_item_create function.

        :param mock_process_order_item: A mock object of the process_order_item function.
        :type mock_process_order_item: MagicMock
        :return: None
        :rtype: NoneType
        """
        # Simulate creating a new OrderItem
        formset = mock.Mock(model=OrderItem)
        form = mock.Mock(
            instance=OrderItem(order=self.order, product=self.product, quantity=1)
        )
        formset.forms = [form]
        mock_form = Mock()
        mock_form.save_m2m = Mock()
        admin = OrderAdmin(model=Order, admin_site=mock.Mock())
        admin.save_related(None, mock_form, [formset], False)  # New order creation

        data = {
            "id": str(form.instance.id),
            "order": str(form.instance.order),
            "product": str(form.instance.product),
            "get_action": str(
                form.instance.get_action
            ),  # Might need to mock this method
            "quantity": str(form.instance.quantity),
        }
        mock_process_order_item.assert_called_once_with(data)

    def test_save_related_calls_process_order_item_update(
        self, mock_process_order_item
    ):
        """
        Test that the save_related method calls the process_order_item_update function when updating an existing OrderItem.

        :param mock_process_order_item: A mock object of the process_order_item function.
        :type mock_process_order_item: MagicMock

        :return: None
        :rtype: None
        """
        # Simulate updating an existing OrderItem
        order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1
        )
        formset = mock.Mock(model=OrderItem)
        mock_form = Mock()
        mock_form.save_m2m = Mock()
        form = mock.Mock(instance=order_item)
        formset.forms = [form]

        admin = OrderAdmin(model=Order, admin_site=mock.Mock())
        admin.save_related(None, mock_form, [formset], True)  # Existing order update

        data = {
            "id": str(order_item.id),
            "order": str(order_item.order),
            "product": str(order_item.product),
            "get_action": str(order_item.get_action),  # Might need to mock this method
            "quantity": str(order_item.quantity),
        }
        mock_process_order_item.assert_called_once_with(data)
