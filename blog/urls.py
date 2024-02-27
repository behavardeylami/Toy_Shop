# urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Template Views
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),  # Update the name to 'post_detail'

    # API Views
    path('api/categories/', views.api_category_list, name='api_category_list'),
    path('api/categories/<int:category_id>/', views.api_category_detail, name='api_category_detail'),
    path('api/posts/', views.api_post_list, name='api_post_list'),
    path('api/posts/<int:post_id>/', views.api_post_detail, name='api_post_detail'),
    path('api/posts/<int:post_id>/comments/', views.api_comment_list, name='api_comment_list'),
    path('api/comments/<int:comment_id>/', views.api_comment_detail, name='api_comment_detail'),
]
