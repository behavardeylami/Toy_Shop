from django.urls import path
from . import views
from .views import add_to_cart

app_name = 'store'

urlpatterns = [
    # Template Views
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),

    # API Views
    path('api/categories/', views.api_category_list, name='api_category_list'),
    path('api/categories/<int:category_id>/', views.api_category_detail, name='api_category_detail'),
    path('api/products/', views.api_product_list, name='api_product_list'),
    path('api/products/<int:product_id>/', views.api_product_detail, name='api_product_detail'),
    path('api/products/<int:product_id>/comments/', views.api_comment_list, name='api_comment_list'),
    path('api/comments/<int:comment_id>/', views.api_comment_detail, name='api_comment_detail'),
]
