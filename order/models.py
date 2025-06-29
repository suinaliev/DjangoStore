from django.db import models
from product.models import Product
from vendor.models import Vendor
from django.contrib.auth.models import User

# Create your models here.
class ShippingMethod(models.Model):
    name = models.CharField('Название', max_length=100)
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
    description = models.TextField('Описание', blank=True)
    estimated_days = models.CharField('Срок доставки', max_length=50)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'

    def __str__(self):
        return f"{self.name} ({self.price} сом)"

class PaymentMethod(models.Model):
    PAYMENT_TYPES = (
        ('stripe', 'Stripe'),
        ('cash', 'Наличные при получении'),
        ('bank_transfer', 'Банковский перевод'),
    )
    
    name = models.CharField('Название', max_length=100)
    payment_type = models.CharField('Тип оплаты', max_length=20, choices=PAYMENT_TYPES)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В обработке'),
        ('processing', 'Обрабатывается'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен')
    )
    
    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Добавляем новые поля
    shipping_method = models.ForeignKey(ShippingMethod, 
                                      verbose_name='Способ доставки',
                                      on_delete=models.SET_NULL,
                                      null=True)
    payment_method = models.ForeignKey(PaymentMethod, 
                                     verbose_name='Способ оплаты',
                                     on_delete=models.SET_NULL,
                                     null=True)
    stripe_token = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        total = sum(item.get_total_price() for item in self.items.all())
        if self.shipping_method:
            total += self.shipping_method.price
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="items", on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name="items", on_delete=models.SET_NULL, null=True)
    vendor_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        return self.price * self.quantity
