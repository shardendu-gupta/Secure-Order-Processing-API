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




class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]

    def get_queryset(self):
        queryset = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')
        if (self.request.user.is_superuser or self.request.user.role in ['STAFF', 'ADMIN']):
            return queryset
        return queryset.filter(user=self.request.user)
    

class OrderDetailsView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]

    def get_queryset(self):
        queryset = Order.objects.select_related('user').prefetch_related('items__product')
        if (self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'STAFF']):
            return queryset
        return queryset.filter(user=self.request.user)




