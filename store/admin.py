from django.contrib import admin
from django.contrib.admin import register, ModelAdmin
from django.contrib import messages
from django.utils.translation import ngettext

from .models import Category, Product, Price, Media, Comment


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

class MyModelAdmin(ModelAdmin):
    actions = (activate_selected_items, deactivate_selected_items,)

# Register My models
@register(Category)
class CategoryAdmin(MyModelAdmin):
    list_display = (
        "is_active",
        "id",
        "name",
        "description",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "name")
    list_filter = ('is_active', 'id', 'name', 'created_at', 'updated_at')
    search_fields = ("title", "description")


@register(Product)
class ProductAdmin(MyModelAdmin):
    list_display = (
        'is_active',
        'id',
        'name',
        'description',
        'category',
        'discount',
        'thumbnail',
        'price',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'name')
    list_filter = ('is_active', 'id', 'name', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'body', 'category__name')



@register(Price)
class PriceAdmin(MyModelAdmin):
    list_display = (
        "is_active",
        "id",
        "product",
        "price",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "product")
    list_filter = ('is_active', 'id', 'created_at', 'updated_at')
    search_fields = ("product__name",)


@register(Media)
class MediaAdmin(MyModelAdmin):
    list_display = (
        'is_active',
        'id',
        'title',
        'description',
        'media_type',
        'file',
        'product',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'title')
    list_filter = ('is_active', 'id', 'title', 'date')
    search_fields = ('title', 'description')



@register(Comment)
class CommentAdmin(MyModelAdmin):
    list_display = (
        'is_active',
        'id',
        'author',
        'product',
        'date',
    )
    list_display_links = ('id', 'author')
    list_filter = (
        'is_active',
        'id',
        'author',
        'created_at',
        'updated_at',
    )
    search_fields = ('author', 'product', 'text', 'date')
