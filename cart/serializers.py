from rest_framework import serializers
from .models import ShoppingBasket, BasketItem
from store.serializers import ProductSerializer  


class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  

    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'quantity', 'order_at']


class ShoppingBasketSerializer(serializers.ModelSerializer):
    basket_items = BasketItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingBasket
        fields = ['id', 'user', 'total_price', 'date_order', 'tracking_code', 'basket_items']
        read_only_fields = ['id', 'user', 'total_price', 'date_order', 'tracking_code', 'basket_items']
