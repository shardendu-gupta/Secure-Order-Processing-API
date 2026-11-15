from rest_framework import serializers
from .models import Inventory, StockMovement
from products.models import Product



class InventorySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True))
    product_name = serializers.CharField(source='product.name', read_only=True)
    availble_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_name', 'quantity', 'reserved_quantity', 'availble_quantity', 'updated_at']
        read_only_fields = ['id', 'reserved_quantity', 'availble_quantity', 'updated_at',]

    def validate_product(self, value):
        if Inventory.objects.filter(product=value).exists():
            raise serializers.ValidationError("Inventory already exists for this product.")
        return value



class StockAdjustmentSerializer(serializers.Serializer):
    movement_type = serializers.ChoiceField(choices=['IN', 'OUT', 'SET'])
    quantity = serializers.IntegerField(min_value=0)
    reason = serializers.CharField(max_length=255, required=False, allow_blank=True)

