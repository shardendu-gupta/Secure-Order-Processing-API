from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['id', 'created_at', 'updated_at']


    def validate(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Product name is required.")
        return value
        