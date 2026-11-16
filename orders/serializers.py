from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from django.db import transaction
from inventory.models import Inventory




class OrderItemInputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True))
    quantity = serializers.IntegerField(min_value=0)


class OderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemInputSerializer(many=True)

    class Meta:
        model = Order
        fields = ['items']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one product is required.")

        product_ids = [item['product'].id for item in value]

        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Duplicate product are not allowed.")
        return value

         
    @transaction
    def create(self, validated_data):

        items_data = validated_data.pop('items')
        product_ids = [item['product'].id for item in items_data]
        inventories = Inventory.objects.select_for_update().select_related('product').filter(product_id__in=product_ids).order_by('id')
        inventory_map = {inventory.product_id: inventory for inventory in inventories}

        for item in items_data:
            product = item['product']
            quantity = item['quantity']
            inventory = inventory_map.get(product.id)

            if not inventory:
                raise serializers.ValidationError(f"Inventory not found for {product.name}.")
            if inventory.available_quantity < quantity:
                raise serializers.ValidationError(f"Insufficient stock for {product.name}.")

        order = Order.objects.create(user=self.context['request'].user)
        total_amount = 0
        for item in items_data:
            product = item['product']
            quantity = item['quantity']
            inventory = inventory_map[product.id]
            subtotal = product.price * quantity

            OrderItem.objects.create(order=order, product=product, quantity=quantity, unit_price=product.price, subtotal=subtotal)

            inventory.reserved_quantity += quantity
            inventory.save()
            total_amount += subtotal

        order.total_amount = total_amount
        order.save()
        return order
    

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    sku = serializers.CharField(source='product.sku', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'sku', 'quantity', 'unit_price', 'subtotal']

