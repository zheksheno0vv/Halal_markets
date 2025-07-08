from django.db import models
from decimal import Decimal
from users.models import *


class SellerProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='seller_profile')
    shop_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='sellers/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.shop_name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='products')
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
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='purchases')
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
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Рейтинг")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} on {self.product}"


class ReviewReply(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='reply')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='review_replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.review}"



