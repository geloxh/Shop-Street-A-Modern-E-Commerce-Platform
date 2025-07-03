from django.contrib import admin
from .models import Order, OrderItem, Payment, Coupon

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'user__email', 'billing_email')
    readonly_fields = ('id', 'order_number', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('id', 'order_number', 'user', 'status', 'payment_status', 'created_at', 'updated_at')
        }),
        ('Billing Information', {
            'fields': ('billing_first_name', 'billing_last_name', 'billing_email', 'billing_phone',
                      'billing_address_line_1', 'billing_address_line_2', 'billing_city', 
                      'billing_state', 'billing_postal_code', 'billing_country')
        }),
        ('Shipping Information', {
            'fields': ('shipping_first_name', 'shipping_last_name', 'shipping_address_line_1', 
                      'shipping_address_line_2', 'shipping_city', 'shipping_state', 
                      'shipping_postal_code', 'shipping_country')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'shipping_cost', 'tax_amount', 'discount_amount', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('notes', 'tracking_number', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'unit_price', 'total_price')
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('order__order_number', 'product_name', 'product_sku')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'status', 'amount', 'transaction_id', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('order__order_number', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'usage_limit', 'used_count', 'is_active', 'valid_until')
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_until')
    search_fields = ('code',)
    readonly_fields = ('used_count', 'created_at')