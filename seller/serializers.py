from rest_framework import serializers
from .models import *


class SellerProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = '__all__'


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    # product_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

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


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class DeliverySerializers(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class DeliveryItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = DeliveryItem
        fields = '__all__'

    def get_total(self, obj):
        return obj.total_price()


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewReplySerializers(serializers.ModelSerializer):
    class Meta:
        model = ReviewReply
        fields = '__all__'


