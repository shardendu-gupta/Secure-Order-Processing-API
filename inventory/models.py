from django.db import models
from products.models import Product
from accounts.models import User
from django.core.validators import MinValueValidator



class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT, related_name='inventory')
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity
    
    def __str__(self):
        return self.product.name


class StockMovement(models.Model):

    class MovementType(models.TextChoices):
        INITIAL = 'INITIAL', 'Initial stock'
        IN = 'IN', 'Stock In'
        OUT = 'OUT', 'Stock Out'
        SET = 'SET', 'Stock Adjustment'

    inventory = models.ForeignKey(Inventory, on_delete=models.PROTECT, related_name='movements')
    movement_type = models.CharField(max_length=10, choices=MovementType.choices)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    previous_quantity = models.PositiveIntegerField()
    new_quantity = models.PositiveIntegerField()
    reason = models.CharField(max_length=255, blank=True)
    performed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='stock_movements')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inventory.product.name} - {self.movement_type}"

    