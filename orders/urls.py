from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.OrderDetailView.as_view(), name='detail'),
    path('<uuid:pk>/invoice/', views.OrderInvoiceView.as_view(), name='invoice'),
    path('payment/success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/cancel/', views.PaymentCancelView.as_view(), name='payment_cancel'),
]