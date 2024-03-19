from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

# from rest_framework import viewsets
from .tasks import process_order, process_order_item
from adrf.views import APIView
import asyncio


class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True, context={"request": request})
        return Response(serializer.data)

    async def post(self, request):
        serializer = OrderSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            order = serializer.save()
            process_order.delay(OrderSerializer(order).data)
            return Response(OrderSerializer(order).data)
        else:
            return Response(serializer.errors, status=400)

    async def put(self, request):
        serializer = OrderSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            order = serializer.save()
            print(OrderSerializer(order).data)
            # process_order.delay(OrderSerializer(order).data)
            return Response(OrderSerializer(order).data)
        else:
            return Response(serializer.errors, status=400)

    async def delete(self, request):
        serializer = OrderSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            order = serializer.save()
            # process_order.delay(OrderSerializer(order).data)
            return Response(OrderSerializer(order).data)
        else:
            return Response(serializer.errors, status=400)


class OrderItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        orderitems = await OrderItem.objects.all()
        return Response(orderitems)

    async def post(self, request):
        serializer = OrderItemSerializer(
            data=request.data["order"], context={"request": request}
        )
        if serializer.is_valid():
            order_item = serializer.save()
            process_order_item.delay(OrderItemSerializer(order_item).data)
            return Response(OrderItemSerializer(order_item).data)
        return Response(serializer.errors, status=400)

    async def put(self, request):
        serializer = OrderItemSerializer(
            data=request.data["order"], context={"request": request}
        )
        if serializer.is_valid():
            order_item = serializer.save()
            process_order_item.delay(OrderItemSerializer(order_item).data)
            return Response(OrderItemSerializer(order_item).data)
        return Response(serializer.errors, status=400)

    async def delete(self, request):
        serializer = OrderItemSerializer(
            data=request.data["order"], context={"request": request}
        )
        if serializer.is_valid():
            order_item = serializer.save()
            process_order_item.delay(OrderItemSerializer(order_item).data)
            return Response(OrderItemSerializer(order_item).data)
        return Response(serializer.errors, status=400)
