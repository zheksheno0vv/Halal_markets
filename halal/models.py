from django.db import models
from users.models import UserProfile

class MainCategory(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category


class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    product_price = models.PositiveSmallIntegerField()
    product_quantity = models.CharField(max_length=36, null=True, blank=True, verbose_name='Количество предметов в упаковке:')
    composition = models.TextField(null=True, blank=True, verbose_name='Состав:')
    action = models.TextField(null=True, blank=True, verbose_name='Действие:')
    expiration_date = models.CharField(max_length=36, null=True, blank=True, verbose_name='Срок годности:')
    package_contents = models.TextField(null=True, blank=True, verbose_name='Комплектация:')
    product_image = models.ImageField(upload_to='product_images/')

    def get_average_rating(self):
        ratings = self.product_review.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class ProductRating(models.Model):
    product_review = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review')
    client = models.ForeignKey(UserProfile, related_name='client_review', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField()

    def __str__(self):
        return f'{self.client} - {self.product_review}'


class RatingImage(models.Model):
    rating_image = models.ImageField(upload_to='rating_images/')


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        return total_price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product} - {self.quantity}'

    def get_total_price(self):
        return self.product.product_price * self.quantity


class Favorite(models.Model):
    favorite_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favorite_user')
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
    user_buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_buyer')