from django.db import models
from blog.models import BaseModel
from store.models import Product
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class ShoppingBasket(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name='User')
    total_price = models.PositiveIntegerField(blank=True, null=True, verbose_name='Order')
    date_order = models.DateTimeField(auto_now_add=True)
    tracking_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='Tracking code')
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.user.username
    
    def update_total_price(self):
        basket_items = BasketItem.objects.filter(order=self)
        total_price = sum(item.product.price.price * item.quantity for item in basket_items)
        self.total_price = total_price
        self.save()


class BasketItem(BaseModel):
    order = models.ForeignKey(ShoppingBasket, on_delete=models.CASCADE, verbose_name='Order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    order_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.order.user.username} - {self.product.name}"
