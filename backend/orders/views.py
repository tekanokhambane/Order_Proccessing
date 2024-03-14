import random
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import viewsets

# from adrf import viewsets
from asgiref.sync import sync_to_async


class AsyncPermission:
    def has_permission(self, request, view) -> bool:
        if random.random() < 0.7:
            return False

        return True


class OrderViewSet(viewsets.ViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data)

        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        order = queryset.filter(pk=pk).first()
        if order:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        return Response({"error": "Order not found"}, status=404)

    def get_queryset(self):
        return Order.objects.all()


class OrderItemViewSet(viewsets.ViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrderItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderItemSerializer(data=request.data["order"])
        if serializer.is_valid():
            order_item = serializer.save()
            return Response(OrderItemSerializer(order_item).data)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        order_item = queryset.filter(pk=pk).first()
        if order_item:
            serializer = OrderItemSerializer(order_item)
            return Response(serializer.data)
        return Response({"error": "Order item not found"}, status=404)

    def get_queryset(self):
        return OrderItem.objects.all()
