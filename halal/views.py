from rest_framework import generics, viewsets
from .models import *
from .serializers import *


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()  # без фильтра parent
    serializer_class = CategorySimpleSerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySimpleSerializer
    lookup_field = 'pk'


class ProductListByCategoryView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'pk'


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemCreateAPIView(generics.CreateAPIView):
    serializer_class = CartItemSerializer


class CartItemListApiView(generics.ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer


class CartItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer


class CartItemStatusListApiView(generics.ListAPIView):
    queryset = CartItem.objects.filter(status='в пути')
    serializer_class = CartItemListSerializer


class CartItemStatusDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.filter(status='в пути')
    serializer_class = CartItemListSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteItemListAPIView(generics.ListAPIView):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer

class FavoriteItemDetailAPIView(generics.RetrieveAPIView):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer



class FavoriteItemCreateAPIView(generics.CreateAPIView):
    serializer_class = FavoriteItemSerializer


class CheckListAPIView(generics.ListAPIView):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer

class CheckCreateAPIView(generics.CreateAPIView):
    serializer_class = CheckSerializer
