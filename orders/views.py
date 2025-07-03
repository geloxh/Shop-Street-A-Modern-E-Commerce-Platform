from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import Order, OrderItem, Payment
from cart.models import Cart
from accounts.models import Address
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/checkout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.filter(user=self.request.user).first()
        
        if not cart or not cart.items.exists():
            messages.error(self.request, 'Your cart is empty')
            return redirect('cart:detail')
        
        context['cart'] = cart
        context['addresses'] = Address.objects.filter(user=self.request.user)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

class OrderCreateView(LoginRequiredMixin, View):
    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        
        if not cart or not cart.items.exists():
            return JsonResponse({'success': False, 'message': 'Cart is empty'})
        
        # Get form data
        billing_address_id = request.POST.get('billing_address')
        shipping_address_id = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        
        billing_address = get_object_or_404(Address, id=billing_address_id, user=request.user)
        shipping_address = get_object_or_404(Address, id=shipping_address_id, user=request.user)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            billing_first_name=billing_address.first_name,
            billing_last_name=billing_address.last_name,
            billing_email=request.user.email,
            billing_phone=billing_address.phone,
            billing_address_line_1=billing_address.address_line_1,
            billing_address_line_2=billing_address.address_line_2,
            billing_city=billing_address.city,
            billing_state=billing_address.state,
            billing_postal_code=billing_address.postal_code,
            billing_country=billing_address.country,
            shipping_first_name=shipping_address.first_name,
            shipping_last_name=shipping_address.last_name,
            shipping_address_line_1=shipping_address.address_line_1,
            shipping_address_line_2=shipping_address.address_line_2,
            shipping_city=shipping_address.city,
            shipping_state=shipping_address.state,
            shipping_postal_code=shipping_address.postal_code,
            shipping_country=shipping_address.country,
            subtotal=cart.total_price,
            total_amount=cart.total_price,
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                variant_name=cart_item.variant.name if cart_item.variant else '',
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=cart_item.total_price,
            )
        
        # Process payment
        if payment_method == 'stripe':
            try:
                # Create Stripe payment intent
                intent = stripe.PaymentIntent.create(
                    amount=int(order.total_amount * 100),  # Convert to cents
                    currency='usd',
                    metadata={'order_id': str(order.id)}
                )
                
                # Create payment record
                Payment.objects.create(
                    order=order,
                    payment_method='stripe',
                    amount=order.total_amount,
                    transaction_id=intent.id,
                )
                
                # Clear cart
                cart.clear()
                
                return JsonResponse({
                    'success': True,
                    'client_secret': intent.client_secret,
                    'order_id': str(order.id)
                })
                
            except stripe.error.StripeError as e:
                order.delete()
                return JsonResponse({'success': False, 'message': str(e)})
        
        return JsonResponse({'success': False, 'message': 'Invalid payment method'})

class PaymentSuccessView(TemplateView):
    template_name = 'orders/payment_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.GET.get('order_id')
        if order_id:
            context['order'] = get_object_or_404(Order, id=order_id, user=self.request.user)
        return context

class PaymentCancelView(TemplateView):
    template_name = 'orders/payment_cancel.html'

class OrderInvoiceView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/invoice.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)