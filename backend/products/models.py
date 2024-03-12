from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductType(models.Model):
    class ActionChoices(models.TextChoices):
        APPROVE = "approve"
        INSPECT = "inspect"
        SHIP = "ship"
        PACKAGE = "package"
        ASSEMBLE = "assemble"

    name = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="product_types"
    )
    action = models.CharField(
        max_length=255, choices=ActionChoices.choices, default="approve"
    )

    class Meta:
        unique_together = ("name", "assigned_to")

    def __str__(self):
        if self.name:
            return self.name
        return "Unnamed ProductType"

    @property
    def get_assigned_user(self):
        return f"{self.assigned_to.first_name} {self.assigned_to.last_name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="products/")
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
