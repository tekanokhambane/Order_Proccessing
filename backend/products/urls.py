from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductTypeViewSet, home
from . import views

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("producttypes", ProductTypeViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.HomeView.as_view(), name="home"),
    path("checkout/", views.HomeView.as_view(), name="checkout"),
]
