from django.contrib import admin, messages
from django.contrib.admin import register
from django.utils.translation import ngettext
from .models import Payment


# Admin actions
@admin.action(description='Activate selected items')
def activate_selected_items(self, request, queryset):
    updated_count = queryset.update(is_paid=True)
    self.message_user(request, ngettext(
        '%d item was successfully activated.',
        '%d items were successfully activated.',
        updated_count,
    ) % updated_count, messages.SUCCESS)


@admin.action(description='Deactivate selected items')
def deactivate_selected_items(self, request, queryset):
    updated_count = queryset.update(is_paid=False)
    self.message_user(request, ngettext(
        '%d item was successfully deactivated.',
        '%d items were successfully deactivated.',
        updated_count,
    ) % updated_count, messages.SUCCESS)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('basket', 'amount', 'payment_status', 'payment_date', 'payment_method')
    list_filter = ('payment_status',)
    search_fields = ('basket__user__username',)  # Assuming there is a ForeignKey from ShoppingBasket to User

    fieldsets = (
        ('General Information', {
            'fields': ('basket', 'amount', 'payment_status', 'payment_date', 'payment_method'),
        }),
    )

    readonly_fields = ('payment_date',)  # Assuming payment_date is automatically set or updated elsewhere

    def get_queryset(self, request):
        # Override queryset to prefetch related data for performance
        return super().get_queryset(request).select_related('basket__user')
