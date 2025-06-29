from django.core.management.base import BaseCommand
from order.models import PaymentMethod

class Command(BaseCommand):
    help = 'Setup payment methods'

    def handle(self, *args, **kwargs):
        # Stripe
        PaymentMethod.objects.get_or_create(
            name='Оплата картой',
            payment_type='stripe',
            description='Безопасная оплата картой через Stripe',
            is_active=True
        )

        # Cash on delivery
        PaymentMethod.objects.get_or_create(
            name='Наличными при получении',
            payment_type='cash',
            description='Оплата наличными курьеру при получении заказа',
            is_active=True
        )

        # Bank transfer
        PaymentMethod.objects.get_or_create(
            name='Банковский перевод',
            payment_type='bank_transfer',
            description='Оплата через банковский перевод по реквизитам',
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS('Successfully set up payment methods')) 