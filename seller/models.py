from enum import unique
from django.db import models
from decimal import Decimal


from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True, region='KG')

    def __str__(self):
        return self.username


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    import random
    code = random.randint(1000, 9999)
    reset_password_token.key = str(code)
    reset_password_token.save()

    send_mail(
        "Сброс пароля",
        f"Ваш код для сброса пароля: {code}",
        "noreply@example.com",
        [reset_password_token.user.email],
        fail_silently=False,
    )




class SellerProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='seller_profile')
    shop_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(unique=True, region='KG')
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='sellers/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_blocked = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Продавец'

    def __str__(self):
        return self.shop_name


class BuyerProfile(models.Model):
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=54)
    last_name = models.CharField(max_length=54)
    image = models.ImageField(upload_to='image_buyer/')
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True, region='KG')

    class Meta:
        verbose_name = 'Клиент'

    def __str__(self):
        return self.first_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')

    product_name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Главное изображение

    ingredients = models.TextField(blank=True)
    expiration_date = models.CharField(max_length=100, blank=True)
    package_content = models.TextField(blank=True)
    effect = models.TextField(blank=True)
    gender = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=50, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
    additional_info = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} ({self.get_discounted_price()})"

    def get_discounted_price(self):
        if self.discount_percent:
            return self.price - (self.price * Decimal(self.discount_percent) / 100)
        return self.price


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')


class Delivery(models.Model):
    STATUS_CHOICES = (
        ('delivered', 'Доставлено'),
        ('in_progress', 'В пути'),
        ('canceled', 'Отменено')
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='deliveries')
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='purchases')
    quantity = models.PositiveIntegerField(default=1)
    delivery_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

    def __str__(self):
        return f"{self.product.product_name} → {self.buyer.username} ({self.status})"


class DeliveryItem(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_items')
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.get_discounted_price()

    def __str__(self):
        return f"{self.product.product_name} × {self.quantity}"


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} on {self.product}"


class ReviewReply(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='reply')
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='review_replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.review}"




