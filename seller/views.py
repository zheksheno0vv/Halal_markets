from rest_framework import viewsets, generics
from .serializers import *
from .models import *


class SellerProfileViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializers


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializers


class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializers


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializers


class DeliveryItemViewSet(viewsets.ModelViewSet):
    queryset = DeliveryItem.objects.all()
    serializer_class = DeliveryItemSerializers


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class ReviewReplyViewSet(viewsets.ModelViewSet):
    queryset = ReviewReply.objects.all()
    serializer_class = ReviewReplySerializers
