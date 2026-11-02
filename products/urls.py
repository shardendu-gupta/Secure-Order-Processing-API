from django.urls import path
from .views import ProductListView, ProductDetailsView

urlpatterns = [

    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailsView.as_view(), name='product-detail'),

]

