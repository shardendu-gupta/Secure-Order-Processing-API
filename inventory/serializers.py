from rest_framework import serializers
from .models import Inventory, StockMovement
from products.models import Product



class InventorySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True))
    product_name = serializers.CharField(source='product.name', read_only=True)
    available_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_name', 'quantity', 'reserved_quantity', 'available_quantity', 'updated_at']
        read_only_fields = ['id', 'reserved_quantity', 'available_quantity', 'updated_at',]

    def validate_product(self, value):
        if Inventory.objects.filter(product=value).exists():
            raise serializers.ValidationError("Inventory already exists for this product.")
        return value



class StockAdjustmentSerializer(serializers.Serializer):
    movement_type = serializers.ChoiceField(choices=['IN', 'OUT', 'SET'])
    quantity = serializers.IntegerField(min_value=0)
    reason = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs['movement_type'] in ['IN', 'OUT'] and attrs['quantity'] == 0:
            raise serializers.ValidationError("Quantity must be greater than zero for stock in or out.")
        return attrs



class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='inventory.product.name', read_only=True)
    performed_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StockMovement
        fields = ['id', 'product_name', 'movement_type', 'quantity', 'previous_quantity', 'new_quantity', 'reason', 'performed_by', 'created_at',]

