from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']


    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Product name is required.")
        return value

    def validate_sku(self, value):
        value = value.strip().upper()
        product = Product.objects.filter(sku__iexact=value)
        if self.instance:
            product = Product.exclude(pk=self.instance.pk)
        if product.exists():
            raise serializers.ValidationError("This SKU already exists.")
        return value

