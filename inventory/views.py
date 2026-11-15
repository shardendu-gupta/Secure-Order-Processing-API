from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Inventory, StockMovement
from .serializers import (InventorySerializer, StockAdjustmentSerializer, StockMovementSerializer,)
from .permissions import InventoryPermission, StockHistoryPermission



class InventoryListView(generics.ListAPIView):
    queryset = Inventory.objects.select_related('product').all()
    serializer_class = InventorySerializer
    permission_classes = [InventoryPermission]


class InventoryCreateView(generics.CreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [InventoryPermission]

    def perform_create(self, serializer):
        inventory = serializer.save()

        StockMovement.objects.create(
                    inventory=inventory,
                    movement_type=StockMovement.MovementType.INITIAL,
                    quantity=inventory.quantity,
                    previous_quantity=0,
                    new_quantity=inventory.quantity,
                    reason='Initial stock',
                    performed_by=self.request.user
                )

class InventoryDetailsView(generics.RetrieveAPIView):
    serializer_class = InventorySerializer
    permission_classes = [InventoryPermission]

    def get_object(self):
        return get_object_or_404(Inventory.objects.select_related('product'), product_id=self.kwargs['product_id'])
    


class StockAdjustmentView(APIView):
    permission_classes = [InventoryPermission]
    def post(self, request, product_id):
        serializer = StockAdjustmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            inventory = get_object_or_404(Inventory.objects.select_for_update(), product_id=product_id)
            movement_type = serializer.validated_data['movement_type']
            quantity = serializer.validated_data['quantity']
            reason = serializer.validated_data.get('reason', '')
            previous_quantity = inventory.quantity

            if movement_type == 'IN':
                new_quantity = previous_quantity + quantity

            elif movement_type == 'OUT':
                new_quantity = previous_quantity - quantity

                if new_quantity < inventory.reserved_quantity:
                    return Response({'message': 'Insufficient available stock.'}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                new_quantity = quantity

                if new_quantity < inventory.reserved_quantity:
                    return Response({'message': 'Stock cannot be lower than reserved quantity.'}, status=status.HTTP_400_BAD_REQUEST)

            inventory.quantity = new_quantity
            inventory.save()

            StockMovement.objects.create(
                inventory=inventory,
                movement_type=movement_type,
                quantity=quantity,
                previous_quantity=previous_quantity,
                new_quantity=new_quantity,
                reason=reason,
                performed_by=request.user
            )

        return Response(
            {
                'message': 'Stock updated successfully.',
                'product': inventory.product.name,
                'previous_quantity': previous_quantity,
                'new_quantity': new_quantity,
                'reserved_quantity': inventory.reserved_quantity,
                'available_quantity': inventory.available_quantity,
            },
            status=status.HTTP_200_OK
        )


class StockMovementListView(generics.ListAPIView):

    serializer_class = StockMovementSerializer
    permission_classes = [StockHistoryPermission]

    def get_queryset(self):
        return StockMovement.objects.filter(inventory__product_id=self.kwargs['product_id']
                                            ).select_related('inventory__product','performed_by').order_by('-created_at')
