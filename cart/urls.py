from django.urls import path
from .views import view_shopping_basket, add_to_basket, remove_from_basket

app_name = 'cart'

urlpatterns = [
    path('view/', view_shopping_basket, name='view_shopping_basket'),
    path('add/<int:product_id>/', add_to_basket, name='add_to_basket'),
    path('remove/<int:basket_item_id>/', remove_from_basket, name='remove_from_basket'),
]
