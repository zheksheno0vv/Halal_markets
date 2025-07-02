from rest_framework import serializers
from .models import *
from users.serializers import UserProfile




class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name', 'email', 'phone_number']


class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_image', 'product_name', 'product_price', 'product_quantity']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = '__all__'


class RatingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingImage
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = CartItem
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['favorite_user', 'created_date']


class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = ['favorite', 'product']


class CheckSerializer(serializers.ModelSerializer):
    user_buyer = UserProfileSimpleSerializer()
    class Meta:
        model = Check
        fields = '__all__'