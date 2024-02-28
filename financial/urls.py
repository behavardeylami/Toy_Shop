from django.urls import path
from .views import payment_form_view, payment_successful, payment_unsuccessful
from .views import PaymentListCreateView, PaymentRetrieveUpdateDestroyView

app_name = 'financial'

urlpatterns = [
    # Template Views
    path('payment-form/', payment_form_view, name='payment_form'),
    path('payment/successful/<int:basket_id>/', payment_successful, name='payment_successful'),
    path('payment/unsuccessful/', payment_unsuccessful, name='payment_unsuccessful'),

    # API Views
    path('api/payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('api/payments/<int:pk>/', PaymentRetrieveUpdateDestroyView.as_view(), name='payment-retrieve-update-destroy'),
]
