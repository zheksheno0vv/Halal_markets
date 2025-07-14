from rest_framework import serializers
from .models import *


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'weight', 'images']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CartItemListSerializer(serializers.ModelSerializer):
    items = ProductListSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'items', 'cart', 'quantity', 'status']


class CartSerializer(serializers.ModelSerializer):
    total_product_count = serializers.SerializerMethodField()
    cart_items = CartItemListSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user_cart', 'total_product_count', 'cart_items']

    def get_total_product_count(self, obj):
        return obj.get_total_product_count()


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = '__all__'

class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'

