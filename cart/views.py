from django.shortcuts import render, get_object_or_404
from .models import ShoppingBasket, BasketItem
from store.models import Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import ShoppingBasket, BasketItem
from .serializers import ShoppingBasketSerializer, BasketItemSerializer


@login_required
def view_shopping_basket(request):
    user_basket = ShoppingBasket.objects.get_or_create(user=request.user)[0]
    basket_items = BasketItem.objects.filter(order=user_basket)

    context = {
        'user_basket': user_basket,
        'basket_items': basket_items,
    }

    return render(request, 'your_template_name.html', context)


@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get or create the user's shopping basket
    user_basket, created = ShoppingBasket.objects.get_or_create(user=request.user)

    # Get or create the basket item for the product in the basket
    basket_item, created = BasketItem.objects.get_or_create(order=user_basket, product=product)

    # Increment the quantity of the basket item
    basket_item.quantity += 1
    basket_item.save()

    # Update total_price after adding a new item
    user_basket.update_total_price()

    return HttpResponseRedirect(reverse('view_shopping_basket'))


@login_required
def remove_from_basket(request, basket_item_id):
    basket_item = get_object_or_404(BasketItem, id=basket_item_id)
    basket_item.delete()

    return HttpResponseRedirect(reverse('view_shopping_basket'))


class ShoppingBasketListCreateView(generics.ListCreateAPIView):
    queryset = ShoppingBasket.objects.all()
    serializer_class = ShoppingBasketSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShoppingBasketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingBasket.objects.all()
    serializer_class = ShoppingBasketSerializer
    permission_classes = [permissions.IsAuthenticated]


class BasketItemCreateView(generics.CreateAPIView):
    serializer_class = BasketItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        user_basket, created = ShoppingBasket.objects.get_or_create(user=self.request.user)
        serializer.save(order=user_basket, product=product)
        user_basket.update_total_price()


class BasketItemDestroyView(generics.DestroyAPIView):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer
    permission_classes = [permissions.IsAuthenticated]