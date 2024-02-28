from django.shortcuts import render, redirect
from django.urls import reverse
from cart.models import ShoppingBasket
from .models import Payment
from rest_framework import viewsets
from .serializers import PaymentSerializer
from rest_framework import generics


def payment_form_view(request):
    # Your payment form logic goes here
    user_basket, created = ShoppingBasket.objects.get_or_create(user=request.user)
    context = {'user_basket': user_basket}

    return render(request, 'financial/payment_form.html', context)


def payment_successful(request, basket_id):
    basket = ShoppingBasket.objects.get(pk=basket_id)
    
    total_price = basket.total_price if basket.total_price else 0
    payment = Payment.objects.create(
        basket=basket,
        amount=total_price,  # Providing the correct value for the amount field
        payment_status=Payment.PaymentStatus.COMPLETED
    )
    
    # Settling the payment and emptying the shopping basket
    basket.update_total_price()
    basket.delete()
    
    return render(request, 'financial/payment_successful.html', {'payment': payment})


def payment_unsuccessful(request):
    # Any actions to be taken in case of an unsuccessful payment can be added here
    return render(request, 'financial/payment_unsuccessful.html')


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer