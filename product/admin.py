from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# Register your models here.

from .models import Category, Product, Brand

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'logo_preview']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'slug', 'description')
        }),
        (_('Изображение'), {
            'fields': ('logo',),
            'classes': ('collapse',)
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.logo.url)
        return '—'
    logo_preview.short_description = _('Логотип')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'product_count']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = _('Количество товаров')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'brand', 'formatted_price', 'image_preview', 'is_popular', 'created_at']
    list_filter = ['category', 'brand', 'is_popular', 'created_at']
    list_editable = ['is_popular']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('title', 'slug', 'description')
        }),
        (_('Категоризация'), {
            'fields': ('category', 'brand', 'is_popular')
        }),
        (_('Цена'), {
            'fields': ('price',),
            'classes': ('wide',)
        }),
        (_('Изображения'), {
            'fields': ('image', 'thumbnail'),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_price(self, obj):
        price_str = '{:,.2f}'.format(float(obj.price))
        return format_html('<span style="color: #28a745; font-weight: bold;">{} сом </span>', price_str)
    formatted_price.short_description = _('Цена')
    formatted_price.admin_order_field = 'price'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.get_thumbnail())
        return '—'
    image_preview.short_description = _('Изображение')

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }