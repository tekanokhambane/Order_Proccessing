from django.db import models


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        CREATED = "created"
        APPROVED = "approved"
        SHIPPED = "shipped"
        DELIVERED = "delivered"
        CANCELED = "canceled"
        PENDING = "pending"

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    shipping_address = models.ForeignKey("address.Address", on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=StatusChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def amount(self):
        total = 0
        for item in self.items.all():
            total += item.product.price * item.quantity
        return total

    def __str__(self):
        return f"Order: {self.pk}, User: {self.user}, Amount: {self.amount}, - Status: {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order} - Product: {self.product}"

    @property
    def get_action(self):
        """
        This function is a property getter that returns the action associated with the product type of the product.
        """
        return self.product.product_type.action
