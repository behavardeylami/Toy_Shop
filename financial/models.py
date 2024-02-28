from django.db import models
from user.models import BaseModel
from cart.models import ShoppingBasket
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class Payment(BaseModel):
    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'

    basket = models.OneToOneField(ShoppingBasket, on_delete=models.CASCADE, verbose_name='Basket', related_name='payment')
    amount = models.PositiveIntegerField(verbose_name='Amount')
    payment_status = models.CharField(
        max_length=20, 
        choices=PaymentStatus.choices, 
        default=PaymentStatus.PENDING, 
        verbose_name='Payment Status'
    )
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='Payment Date')
    payment_method = models.CharField(max_length=50, null=True, blank=True, verbose_name='Payment Method')

    class Meta:
        app_label = 'financial'
        
    def __str__(self):
        return f"{self.basket.user.username} - {self.amount} - {self.payment_status}"
