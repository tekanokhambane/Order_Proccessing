from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductTypeViewSet

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("producttypes", ProductTypeViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
