from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product



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
         







