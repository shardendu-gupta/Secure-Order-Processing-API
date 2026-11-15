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

