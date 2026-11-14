from django.contrib import admin
from .models import Product




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'price', 'is_active', 'created_at',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'sku')
    ordering = ('-created_at',)
