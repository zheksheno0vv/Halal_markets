from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'favorite', FavoriteViewSet, basename='favorite')



urlpatterns = [
    path('', include(router.urls)),
    path('cart_item/create/', CartItemCreateAPIView.as_view(), name='cart_item_create'),
    path('cart_item/', CartItemListApiView.as_view(), name='cart_item_list'),
    path('cart_item/<int:pk>/', CartItemDetailAPIView.as_view(), name='cart_item_detail'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:category_id>/products/', ProductListByCategoryView.as_view(), name='products-by-category'),

    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('cart_status/', CartItemStatusListApiView.as_view(), name='cart_current_status'),
    path('cart_status/<int:pk>/', CartItemStatusDetailApiView.as_view(), name='cart_current_status_detail'),

    path('fav_item/', FavoriteItemListAPIView.as_view(), name='fav_item_list'),
    path('fav_item/<int:pk>/', FavoriteItemDetailAPIView.as_view(), name='fav_item_detail'),
    path('fav_item/create/', FavoriteItemCreateAPIView.as_view(), name='fav_item_create'),

    path('check/', CheckListAPIView.as_view(), name='check_list'),
    path('check/<int:pk>/', CheckCreateAPIView.as_view(), name='check_detail'),
]
