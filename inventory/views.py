from rest_framework import generics
from . models import Inventory
from .serializers import InventorySerializer
from .permissions import InventoryPermission


class InventoryListView(generics.ListAPIView):
    queryset = Inventory.objects.select_related('product').all()
    serializer_class = InventorySerializer
    permission_classes = [InventoryPermission]




