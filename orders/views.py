from rest_framework import generics, status
from rest_framework.views import APIView
from .permissions import OrderPermission, OrderStaffPermission
from .serializers import OrderSerializer, OrderItemSerializer, OrderStatusSerializer, OrderCreateSerializer
from rest_framework.response import Response
from .models import Order
from django.db import transaction
from django.shortcuts import get_object_or_404
from inventory.models import Inventory




class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [OrderPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({'message':'Order create successfully.', 'order':OrderSerializer(order).data}, status=status.HTTP_201_CREATED)






