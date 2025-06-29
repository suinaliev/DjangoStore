from django.contrib import admin
from .models import Order, OrderItem, ShippingMethod, PaymentMethod

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'paid', 'created_at', 'shipping_method', 'payment_method']
    list_filter = ['paid', 'created_at', 'shipping_method', 'payment_method']
    search_fields = ['first_name', 'last_name', 'email']
    inlines = [OrderItemInline]

@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'estimated_days', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'payment_type', 'is_active']
    list_filter = ['payment_type', 'is_active']
    search_fields = ['name', 'description']