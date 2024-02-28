from rest_framework import serializers
from .models import ShoppingBasket, BasketItem


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = '__all__'


class ShoppingBasketSerializer(serializers.ModelSerializer):
    basket_items = BasketItemSerializer(many=True, read_only=True)

    class Meta:
        model = ShoppingBasket
        fields = '__all__'
