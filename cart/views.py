from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Cart, CartItem, Wishlist, WishlistItem
from products.models import Product, ProductVariant

class CartView(TemplateView):
    template_name = 'cart/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_cart()
        context['cart'] = cart
        return context
    
    def get_cart(self):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            cart, created = Cart.objects.get_or_create(session_key=self.request.session.session_key)
        return cart

@method_decorator(csrf_exempt, name='dispatch')
class AddToCartView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        variant_id = request.POST.get('variant_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        variant = None
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id)
        
        # Get or create cart
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Product added to cart',
                'cart_items_count': cart.total_items
            })
        
        messages.success(request, 'Product added to cart successfully!')
        return redirect('cart:detail')

@method_decorator(csrf_exempt, name='dispatch')
class UpdateCartView(View):
    def post(self, request):
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        # Verify ownership
        if request.user.is_authenticated:
            if cart_item.cart.user != request.user:
                return JsonResponse({'success': False, 'message': 'Unauthorized'})
        else:
            if cart_item.cart.session_key != request.session.session_key:
                return JsonResponse({'success': False, 'message': 'Unauthorized'})
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Cart updated',
                'cart_items_count': cart_item.cart.total_items,
                'cart_total': str(cart_item.cart.total_price)
            })
        
        return redirect('cart:detail')

class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        # Verify ownership
        if request.user.is_authenticated:
            if cart_item.cart.user != request.user:
                messages.error(request, 'Unauthorized action')
                return redirect('cart:detail')
        else:
            if cart_item.cart.session_key != request.session.session_key:
                messages.error(request, 'Unauthorized action')
                return redirect('cart:detail')
        
        cart_item.delete()
        messages.success(request, 'Item removed from cart')
        return redirect('cart:detail')

class ClearCartView(View):
    def post(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = Cart.objects.filter(session_key=request.session.session_key).first()
        
        if cart:
            cart.clear()
            messages.success(request, 'Cart cleared successfully')
        
        return redirect('cart:detail')

class WishlistView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/wishlist.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wishlist, created = Wishlist.objects.get_or_create(user=self.request.user)
        context['wishlist'] = wishlist
        return context

class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist_item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            product=product
        )
        
        if created:
            message = 'Product added to wishlist'
        else:
            message = 'Product already in wishlist'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': message,
                'in_wishlist': True
            })
        
        messages.success(request, message)
        return redirect('products:detail', slug=product.slug)

class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
        wishlist_item.delete()
        messages.success(request, 'Item removed from wishlist')
        return redirect('cart:wishlist')