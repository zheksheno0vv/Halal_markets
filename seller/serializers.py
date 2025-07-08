from rest_framework import serializers
from .models import *


class SellerProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['id', 'user', 'image', 'full_name', 'shop_name', 'email', 'phone_number', 'description']


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    product_images = ProductImageSerializers(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'seller', 'category', 'product_name', 'brand_name', 'country', 'code', 'image', 'ingredients',
                  'expiration_date', 'package_content', 'effect', 'gender', 'color', 'price', 'discount_percent',
                  'additional_info', 'created_at']

    def get_discounted_price(self, obj):
        return obj.get_discounted_price()


class ProductListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class DeliverySerializers(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'product', 'buyer', 'quantity', 'delivery_date', 'created_at', 'status']


class DeliveryItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = DeliveryItem
        fields = ['id', 'delivery', 'product', 'quantity']

    def get_total(self, obj):
        return obj.total_price()


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'text', 'rating', 'created_at']


class ReviewReplySerializers(serializers.ModelSerializer):
    class Meta:
        model = ReviewReply
        fields = ['id', 'review', 'seller', 'text', 'created_at']


