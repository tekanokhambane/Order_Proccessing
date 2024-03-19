# from rest_framework import serializers

from adrf import serializers
from rest_framework.serializers import ValidationError
from .models import Order, OrderItem
from address.models import Address
from accounts.models import Customer, User


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            # "user",
            # "shipping_address",
            "amount",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        # validate the user
        if not self.context["request"].user.is_authenticated:
            raise ValidationError("User not authenticated")
        user = self.context["request"].user
        validated_data["user"] = user
        # validate shipping address
        shpping_address = Customer.objects.get(user=user.id).default_shipping_address
        validated_data["shipping_address"] = shpping_address
        return super().create(validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product",
            "get_action",
            "quantity",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        if not self.context["request"].user.is_authenticated:
            raise ValidationError("User not authenticated")
        return super().create(validated_data)
