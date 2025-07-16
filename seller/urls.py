from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'seller', SellerProfileViewSet, basename='seller-list')
router.register(r'buyer', BuyerProfileViewSet, basename='buyer_list')
router.register(r'category', CategoryViewSet, basename='category-list')
router.register(r'product', ProductViewSet, basename='product-list')
router.register(r'image', ProductViewSet, basename='image-list')
router.register(r'delivery', DeliveryViewSet, basename='delivery-list')
router.register(r'item', DeliveryItemViewSet, basename='item-list')
router.register(r'review', ReviewViewSet, basename='review-list')
router.register(r'reply', ReviewReplyViewSet, basename='reply-list')
router.register(r'sellers', SellerAdminViewSet, basename = 'sellers')



urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductListApiView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailApiView.as_view(), name='product_detail'),
    path('stats/', seller_stats, name='seller-stats'),


    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password_reset/verify_code/', verify_reset_code, name='verify_reset_code'),
    path('user/', UserProfilesListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfilesDetailAPIView.as_view(), name='user_detail'),
]
