from rest_framework import generics, viewsets
from .models import *
from .serializers import *





class MainCategoryViewSet(viewsets.ModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer


class RatingImageViewSet(viewsets.ModelViewSet):
    queryset = RatingImage.objects.all()
    serializer_class = RatingImageSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class  = CartItemSerializer



class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer

class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
