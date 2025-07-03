from .models import Cart

def cart(request):
    """Add cart information to all templates"""
    cart_obj = None
    cart_items_count = 0
    
    try:
        if request.user.is_authenticated:
            cart_obj, created = Cart.objects.get_or_create(user=request.user)
        else:
            # Ensure session exists
            if not request.session.session_key:
                request.session.save()
            if request.session.session_key:
                cart_obj, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        
        if cart_obj:
            cart_items_count = cart_obj.total_items
    except Exception:
        # Fallback to prevent template errors
        cart_obj = None
        cart_items_count = 0
    
    return {
        'cart': cart_obj,
        'cart_items_count': cart_items_count,
    }