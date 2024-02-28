from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from .models import ShoppingBasket, BasketItem


# Admin actions
@admin.action(description='Activate selected items')
def activate_selected_items(modeladmin, request, queryset):
    updated_count = queryset.update(is_active=True)
    modeladmin.message_user(request, ngettext(
        '%d item was successfully activated.',
        '%d items were successfully activated.',
        updated_count,
    ) % updated_count, messages.SUCCESS)


@admin.action(description='Deactivate selected items')
def deactivate_selected_items(modeladmin, request, queryset):
    updated_count = queryset.update(is_active=False)
    modeladmin.message_user(request, ngettext(
        '%d item was successfully deactivated.',
        '%d items were successfully deactivated.',
        updated_count,
    ) % updated_count, messages.SUCCESS)


# Register models
@admin.register(ShoppingBasket)
class ShoppingBasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'date_order', 'tracking_code')
    search_fields = ('user__username',)
    readonly_fields = ['total_price']

    def display_total_price(self, obj):
        return obj.total_price if obj.total_price is not None else 0

    display_total_price.short_description = 'Total Price'
    # admin.site.register(ShoppingBasket, ShoppingBasketAdmin)



@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'product', 'quantity', 'order_at')
    search_fields = ('order__user__username', 'product__name', 'order__tracking_code', 'order__user__email')
    list_filter = ('order__user', 'order__date_order')

    def user(self, obj):
        return obj.order.user.username
    user.short_description = 'User'

    def order(self, obj):
        return f"{obj.order.user.username} - {obj.order.tracking_code}"
    order.short_description = 'Order'
