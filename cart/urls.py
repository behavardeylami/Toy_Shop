from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Views for HTML templates
    path('', views.cart_summary, name='cart_summary'),
    path('add/', views.cart_add, name='cart_add'),

    # # API Endpoints
    path('api/cart/summary/', views.cart_summary_api, name='cart_summary_api'),
    path('api/cart/add/', views.cart_add_api, name='cart_add_api'),
]
