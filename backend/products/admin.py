from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, ProductType


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "image_preview", "product_type", "price"]
    readonly_fields = ("image_preview",)

    # image

    def image_preview(self, obj):

        if obj.image:
            return mark_safe(
                '<img src="{0}" width="150" height="100" style="object-fit:contain" />'.format(
                    obj.image.url
                )
            )
        else:
            return "(No image)"

    image_preview.short_description = "Preview"

    def product_type(self, obj):
        return obj.product_type.name


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_assigned_user",
        "action",
        # "assigned_to",
    )
    list_filter = ("assigned_to",)
    search_fields = ("name", "get_assigned_user")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "action",
                    "assigned_to",
                )
            },
        ),
    )
