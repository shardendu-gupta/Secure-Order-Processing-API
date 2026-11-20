from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from .models import Product
from .serializers import ProductSerializer
from .permissions import ProductPermission




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


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

