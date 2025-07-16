from rest_framework import serializers
from .models import *


class SellerProfileSerializers(serializers.ModelSerializer):
    is_blocked = serializers.BooleanField(source='user.is_blocked', read_only=True)
    class Meta:
        model = SellerProfile
        fields = ['id', 'user', 'image', 'full_name', 'shop_name', 'email', 'phone_number', 'description', 'is_blocked']


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




from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django_rest_passwordreset.models import ResetPasswordToken
from django.contrib.auth import authenticate


User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password')

        if not username and not email:
            raise serializers.ValidationError("Необходимо указать username или email")

        try:
            user = User.objects.get(email=email) if email else User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        if not user.check_password(password):
            raise serializers.ValidationError("Неверный пароль")

        if not user.is_active:
            raise serializers.ValidationError("Пользователь не активен")

        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)
        return {
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль введён неверно.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        reset_code = data.get('reset_code')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают.")

        try:
            token = ResetPasswordToken.objects.get(user__email=email, key=str(reset_code))
        except ResetPasswordToken.DoesNotExist:
            raise serializers.ValidationError("Неверный код сброса или email.")

        data['user'] = token.user
        data['token'] = token
        return data

    def save(self):
        user = self.validated_data['user']
        token = self.validated_data['token']
        new_password = self.validated_data['new_password']

        user.set_password(new_password)
        user.save()
        token.delete()


class UserProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class BuyerProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = '__all__'
