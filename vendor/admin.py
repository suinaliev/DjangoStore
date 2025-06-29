from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Vendor model registration is removed to hide it from admin panel
# from .models import Vendor

# @admin.register(Vendor)
# class VendorAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created_by', 'created_at', 'get_balance', 'get_paid_amount']
#     list_filter = ['created_at']
#     search_fields = ['name', 'created_by__username', 'created_by__email']
#     date_hierarchy = 'created_at'
#     
#     fieldsets = (
#         (_('Основная информация'), {
#             'fields': ('name', 'created_by')
#         }),
#     )
#     
#     def get_balance(self, obj):
#         return f"${obj.get_balance()}"
#     get_balance.short_description = _('Баланс')
#     
#     def get_paid_amount(self, obj):
#         return f"${obj.get_paid_amount()}"
#     get_paid_amount.short_description = _('Оплаченная сумма')
