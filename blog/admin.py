from django.contrib import admin
from django.contrib.admin import register
from django.contrib import messages
from django.utils.translation import ngettext

from .models import Category, Post, Media, Comment


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


# Register My models
@register(Category)
class CategoryAdmin(admin.ModelAdmin):
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
    actions = (activate_selected_items, deactivate_selected_items,)


@register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'is_active',
        'id',
        'title',
        'body',
        'category',
        'author',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'title')
    list_filter = ('is_active', 'id', 'title', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'body', 'category__name')

    actions = (activate_selected_items, deactivate_selected_items)


@register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        'is_active',
        'id',
        'title',
        'description',
        'media_type',
        'file',
        'post',
        'created_at',
        'updated_at'
    )
    list_display_links = ('id', 'title')
    list_filter = ('is_active', 'id', 'title', 'date')
    search_fields = ('title', 'description')

    actions = (activate_selected_items, deactivate_selected_items)


@register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'is_active',
        'id',
        'author',
        'post',
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
    search_fields = ('author', 'post', 'text', 'date')

    actions = (activate_selected_items, deactivate_selected_items)
