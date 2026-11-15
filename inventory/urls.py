from django.urls import path
from .views import InventoryListView, InventoryCreateView, InventoryDetailView, StockAdjustmentView, StockMovementListView


urlpatterns = [

    path('', InventoryListView.as_view(), name='inventory-list'),
    path('create/', InventoryCreateView.as_view(), name='inventory-create'),
    path('<int:product_id>/', InventoryDetailView.as_view(), name='inventory-detail'),
    path('<int:product_id>/adjust/', StockAdjustmentView.as_view(), name='stock-adjust'),
    path('<int:product_id>/movements/', StockMovementListView.as_view(), name='stock-movements'),

]