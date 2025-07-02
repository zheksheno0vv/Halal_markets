from .views import *
from rest_framework import routers
from django.urls import path, include


routers = routers.SimpleRouter()

routers.register(r'mainc', MainCategoryViewSet, basename='main_category')
routers.register(r'category', CartItemViewSet, basename='categories')
routers.register(r'rating', ProductRatingViewSet, basename='ratings')
routers.register(r'cart', CartViewSet, basename='carts')
routers.register(r'cart_item', CartItemViewSet, basename='item_cart')
routers.register(r'favorite', FavoriteViewSet, basename='favorite')
routers.register(r'favorite_item', FavoriteItemViewSet, basename='favorite_item')
routers.register(r'check', CheckViewSet, basename='check')



urlpatterns = [
    path('', include(routers.urls)),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),


]
