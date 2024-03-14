from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet)
router.register("orderitems", OrderItemViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
