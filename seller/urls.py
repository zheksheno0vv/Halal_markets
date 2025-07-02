from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'seller', SellerProfileViewSet, basename='seller-list')
router.register(r'category', CategoryViewSet, basename='category-list')
router.register(r'product', ProductViewSet, basename='product-list')
router.register(r'image', ProductViewSet, basename='image-list')
router.register(r'delivery', DeliveryViewSet, basename='delivery-list')
router.register(r'item', DeliveryItemViewSet, basename='item-list')
router.register(r'review', ReviewViewSet, basename='review-list')
router.register(r'reply', ReviewReplyViewSet, basename='reply-list')



urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductListApiView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailApiView.as_view(), name='product_detail'),
]
