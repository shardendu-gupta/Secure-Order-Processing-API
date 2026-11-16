from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product



class OrderItemInputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True))
    quantity = serializers.IntegerField(min_value=0)











    