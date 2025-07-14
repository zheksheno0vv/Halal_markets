from django.db import models
from django.contrib.auth.models import User
from seller.models import *
from users.models import UserProfile
from django.db.models import Sum


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    expiration_period = models.PositiveIntegerField(default=12, verbose_name='срок годности')
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Вес продукта (в кг)', null=True, blank=True)
    composition = models.TextField(verbose_name='состав', null=True, blank=True)
    storage_condition = models.TextField(verbose_name='условия хранение', null=True, blank=True)
    equipment = models.TextField(null=True, blank=True, verbose_name='комплектация')
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='количество', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/")


class Customer(models.Model):
    user = models.OneToOneField(BuyerProfile, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'В ожидании'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён')
    ], default='pending')

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user_cart = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='buyer_carts')

    class Meta:
        unique_together = ('user_cart',)

    def get_total_product_count(self):
        return self.cart_items.aggregate(total=Sum('quantity'))['total'] or 0

    def __str__(self):
        return f'{self.user_cart}'


class CartItem(models.Model):
    items = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('Доставлено', 'Доставлено'),
        ('в пути', 'в пути'),
        ('в ожидании', 'в ожидании'),
        ('отменен', "отменен")
    )
    status = models.CharField(max_length=34, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.cart}, {self.items}, {self.quantity}'



class Favorite(models.Model):
    favorite_user = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='favorite_user')
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.favorite_user}'


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='clothes_favorite')

    def __str__(self):
        return f'{self.product}'


class Check(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=64)
    date_purchase = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(auto_now_add=True)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='check_product')
    quantity = models.PositiveSmallIntegerField(default=1)
    delivery = models.CharField(max_length=32)
    delivery_text = models.CharField(max_length=32)
    user_buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='user_buyer')
