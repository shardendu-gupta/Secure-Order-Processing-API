from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from inventory.models import Inventory, StockMovement
from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer, OrderStatusSerializer
from .permissions import OrderPermission, OrderStaffPermission




class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [OrderPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({'message': 'Order created successfully.', 'order': OrderSerializer(order).data}, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]

    def get_queryset(self):
        queryset = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')
        if self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'STAFF']:
            return queryset
        return queryset.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]

    def get_queryset(self):
        queryset = Order.objects.select_related('user').prefetch_related('items__product')
        if self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'STAFF']:
            return queryset
        return queryset.filter(user=self.request.user)


class OrderCancelView(APIView):
    permission_classes = [OrderPermission]

    def post(self, request, pk):
        with transaction.atomic():
            order = get_object_or_404(Order.objects.select_for_update(), pk=pk, user=request.user)
            if order.status != Order.Status.PENDING:
                return Response({'message': 'Only pending orders can be cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
            items = order.items.all()
            inventories = Inventory.objects.select_for_update().filter(product_id__in=items.values_list('product_id', flat=True)).order_by('id')
            inventory_map = {inventory.product_id: inventory for inventory in inventories}
            for item in items:
                inventory = inventory_map[item.product_id]
                inventory.reserved_quantity -= item.quantity
                inventory.save()
            order.status = Order.Status.CANCELLED
            order.save()
        return Response({'message': 'Order cancelled successfully.'}, status=status.HTTP_200_OK)


class OrderStatusUpdateView(APIView):
    permission_classes = [OrderStaffPermission]

    def patch(self, request, pk):
        serializer = OrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data['status']
        allowed_transitions = {
            Order.Status.PENDING: [Order.Status.CONFIRMED, Order.Status.CANCELLED],
            Order.Status.CONFIRMED: [Order.Status.PROCESSING, Order.Status.CANCELLED],
            Order.Status.PROCESSING: [Order.Status.SHIPPED],
            Order.Status.SHIPPED: [Order.Status.DELIVERED],
            Order.Status.DELIVERED: [],
            Order.Status.CANCELLED: [],
        }
        with transaction.atomic():
            order = get_object_or_404(Order.objects.select_for_update(), pk=pk)
            if new_status not in allowed_transitions[order.status]:
                return Response({'message': 'Invalid order status transition.'}, status=status.HTTP_400_BAD_REQUEST)
            if new_status == Order.Status.CANCELLED:
                items = order.items.all()
                inventories = Inventory.objects.select_for_update().filter(product_id__in=items.values_list('product_id', flat=True)).order_by('id')
                inventory_map = {inventory.product_id: inventory for inventory in inventories}
                for item in items:
                    inventory = inventory_map[item.product_id]
                    inventory.reserved_quantity -= item.quantity
                    inventory.save()
            if new_status == Order.Status.PROCESSING:
                items = order.items.all()
                inventories = Inventory.objects.select_for_update().filter(product_id__in=items.values_list('product_id', flat=True)).order_by('id')
                inventory_map = {inventory.product_id: inventory for inventory in inventories}
                for item in items:
                    inventory = inventory_map[item.product_id]
                    if inventory.reserved_quantity < item.quantity or inventory.quantity < item.quantity:
                        return Response({'message': 'Reserved stock is not available.'}, status=status.HTTP_400_BAD_REQUEST)
                for item in items:
                    inventory = inventory_map[item.product_id]
                    previous_quantity = inventory.quantity
                    inventory.quantity -= item.quantity
                    inventory.reserved_quantity -= item.quantity
                    inventory.save()
                    StockMovement.objects.create(inventory=inventory, movement_type=StockMovement.MovementType.OUT, quantity=item.quantity, 
                                                 previous_quantity=previous_quantity, new_quantity=inventory.quantity, 
                                                 reason=f'Order {order.order_number} processing', performed_by=request.user)
            order.status = new_status
            order.save()
        return Response({'message': 'Order status updated successfully.', 'order': OrderSerializer(order).data}, status=status.HTTP_200_OK)


    