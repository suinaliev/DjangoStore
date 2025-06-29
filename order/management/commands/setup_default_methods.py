from django.core.management.base import BaseCommand
from order.models import ShippingMethod, PaymentMethod

class Command(BaseCommand):
    help = 'Setup default shipping and payment methods'

    def handle(self, *args, **kwargs):
        # Create default shipping methods if none exist
        if not ShippingMethod.objects.exists():
            ShippingMethod.objects.create(
                name='Стандартная доставка',
                price=200,
                description='Доставка в течение 3-5 рабочих дней',
                estimated_days='3-5 дней',
                is_active=True
            )
            ShippingMethod.objects.create(
                name='Экспресс доставка',
                price=400,
                description='Доставка на следующий рабочий день',
                estimated_days='1-2 дня',
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Созданы стандартные методы доставки'))

        # Create default payment methods if none exist
        if not PaymentMethod.objects.exists():
            PaymentMethod.objects.create(
                name='Оплата картой',
                payment_type='stripe',
                description='Безопасная оплата банковской картой',
                is_active=True
            )
            PaymentMethod.objects.create(
                name='Наличными при получении',
                payment_type='cash',
                description='Оплата наличными курьеру при получении заказа',
                is_active=True
            )
            PaymentMethod.objects.create(
                name='Банковский перевод',
                payment_type='bank_transfer',
                description='Оплата через банковский перевод',
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS('Созданы стандартные методы оплаты')) 