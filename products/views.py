from rest_framework import generics, filters
from .serializers import ProductSerializer
from .models import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .permissions import ProductPermisson





class ProductPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [ProductPermisson]
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']


class ProductDetailsView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [ProductPermisson]


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductPermisson]


class ProductUpdateView(generics.UpdateAPIView):
    queryset = ProductSerializer
    serializer_class = ProductSerializer
    permission_classes = [ProductPermisson]


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductPermisson]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
