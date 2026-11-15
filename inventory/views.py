from rest_framework import generics
from . models import Inventory, StockMovement
from .serializers import InventorySerializer
from .permissions import InventoryPermission



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

