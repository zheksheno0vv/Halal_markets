from django.contrib import admin
from .models import *


admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductRating)
admin.site.register(RatingImage)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)
admin.site.register(Check)