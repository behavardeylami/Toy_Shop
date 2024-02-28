from django.urls import path
from .views import (
    ShoppingBasketListCreateView,
    ShoppingBasketDetailView,
    BasketItemCreateView,
    BasketItemDestroyView,
    view_shopping_basket,
    add_to_basket,
    remove_from_basket,
)

app_name = 'cart'

urlpatterns = [
    # Template Views
    path('view/', view_shopping_basket, name='view_shopping_basket'),
    path('add/<int:product_id>/', add_to_basket, name='add_to_basket'),
    path('remove/<int:basket_item_id>/', remove_from_basket, name='remove_from_basket'),

    # API Views
    path('api/shopping_baskets/', ShoppingBasketListCreateView.as_view(), name='shopping_basket-list-create'),
    path('api/shopping_baskets/<int:pk>/', ShoppingBasketDetailView.as_view(), name='shopping_basket-detail'),
    path('api/basket_items/<int:product_id>/', BasketItemCreateView.as_view(), name='basket_item-create'),
    path('api/basket_items/<int:pk>/', BasketItemDestroyView.as_view(), name='basket_item-destroy'),
]
