from django.db import transaction
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductSerializer
from .permissions import ProductPermission
from audit.utils import create_audit_log




class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]

    def perform_create(self, serializer):
        with transaction.atomic():
            product = serializer.save()
            create_audit_log(self.request, 'CREATE', 'Product', product.id, f"Product {product.name} created.")


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]

    def perform_update(self, serializer):
        with transaction.atomic():
            product = serializer.save()
            create_audit_log(self.request, 'UPDATE', 'Product', product.id, f"Product {product.name} updated.")


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_active = False
            instance.save()
            create_audit_log(self.request, 'DELETE', 'Product', instance.id, f"Product {instance.name} deactivated.")

