from django.urls import path
from . import views

urlpatterns = [
    path("api/orders/", views.OrderAPIView.as_view(), name="get_orders"),
    path("api/orderitems/", views.OrderItemAPIView.as_view(), name="get_orderitems"),
]
