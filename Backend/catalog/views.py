# pylint: disable=no-member
from rest_framework import generics, permissions
from django.utils.translation import gettext_lazy as _
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


# 🟢 Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories or create a new one.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


#Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    """
    List all products or create a new product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductsByCategoryView(generics.ListAPIView):
    """
    List all products under a specific category.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['pk']
        return Product.objects.filter(category_id=category_id)
