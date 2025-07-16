from django.contrib import admin
from .models import *
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import SellerProfile, UserProfile
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from .models import SellerProfile

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'full_name', 'email', 'phone_number', 'is_blocked')
    list_filter = ('is_blocked',)
    search_fields = ('shop_name', 'full_name', 'email', 'phone_number')

    actions = ['block_sellers', 'unblock_sellers']

    def block_sellers(self, request, queryset):
        updated = queryset.update(is_blocked=True)
        self.message_user(request, f"{updated} продавцов заблокированы.")
    block_sellers.short_description = "Заблокировать выбранных продавцов"

    def unblock_sellers(self, request, queryset):
        updated = queryset.update(is_blocked=False)
        self.message_user(request, f"{updated} продавцов разблокированы.")
    unblock_sellers.short_description = "Разблокировать выбранных продавцов"






admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Delivery)
admin.site.register(DeliveryItem)
admin.site.register(Review)
admin.site.register(ReviewReply)
admin.site.register(UserProfile)
admin.site.register(BuyerProfile)





