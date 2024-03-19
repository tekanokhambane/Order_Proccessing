import json
from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from .models import Order, OrderItem
from .tasks import process_order, process_order_item
from tasks.models import Task
from address.models import Address

User = get_user_model()


class OrderForm(forms.ModelForm):
    # status = forms.ChoiceField(choices=Order.STATUS_CHOICES)
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False))

    class Meta:
        model = Order
        fields = ["status", "shipping_address", "user"]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "amount",
        "shipping_address",
        "status",
        "created_at",
        "updated_at",
    ]
    list_filter = ["status"]
    form = OrderForm
    inlines = [OrderItemInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        order_items = []
        for formset in formsets:
            if formset.model == OrderItem:
                for form in formset.forms:
                    if form.cleaned_data:
                        order_items.append(form.instance.product.name)
        order_item_id = form.instance.id
        order = form.instance.order
        product = form.instance.product
        get_action = form.instance.get_action
        quantity = form.instance.quantity
        data = {
            "id": f"{order_item_id}",
            "order": f"{order}",
            "product": f"{product}",
            "get_action": f"{get_action}",
            "quantity": f"{quantity}",
        }
        if not change:  # Check if creating
            process_order_item.delay(data)
        else:
            process_order_item.delay(data)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        data = {
            "id": f"{obj.id}",
            "status": f"{obj.status}",
            "user": f"{obj.user.id}",
            "shipping_address": f"{obj.shipping_address.id}",
            "amount": f"{obj.amount}",
        }
        if not change:  # Check if creating
            process_order.delay(data)
        return HttpResponseRedirect("/admin/orders/order/")
