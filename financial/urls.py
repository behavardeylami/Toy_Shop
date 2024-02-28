from django.urls import path
from .views import payment_form_view, payment_successful, payment_unsuccessful

app_name = 'financial'

urlpatterns = [
    path('payment-form/', payment_form_view, name='payment_form'),
    path('payment/successful/<int:basket_id>/', payment_successful, name='payment_successful'),
    path('payment/unsuccessful/', payment_unsuccessful, name='payment_unsuccessful'),
]
