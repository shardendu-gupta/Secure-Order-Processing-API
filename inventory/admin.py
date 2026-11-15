from django.contrib import admin
from .models import Inventory, StockMovement



@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'reserved_quantity', 'updated_at')
    search_fields = ('product__name', 'product__sku')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('id', 'inventory', 'movement_type', 'quantity', 'previous_quantity', 'new_quantity', 'performed_by', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('inventory__product__name',)
    readonly_fields = ('inventory', 'movement_type', 'quantity', 'previous_quantity', 'new_quantity', 'reason', 'performed_by', 'created_at')

