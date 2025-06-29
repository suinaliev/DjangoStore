from cart.cart import Cart

from django.conf import settings
# for HTML Email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Order, OrderItem

def checkout(request, first_name, last_name, email, address, zipcode, place, phone, amount):
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        first_name=first_name,
        last_name=last_name,
        email=email,
        address=address,
        zipcode=zipcode,
        place=place,
        phone=phone,
        paid_amount=amount,
        status='pending'
    )

    for item in Cart(request):
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            vendor=item['product'].vendor,
            price=item['product'].price,
            quantity=item['quantity']
        )
        order.vendors.add(item['product'].vendor)
        
    return order

def notify_vendor(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    for vendor in order.vendors.all():
        to_email = vendor.created_by.email
        subject = 'Новый заказ'
        text_content = 'У вас новый заказ!'
        html_content = render_to_string('order/email_notify_vendor.html', {'order': order, 'vendor': vendor})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def notify_customer(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.email
    subject = 'Подтверждение заказа'
    text_content = 'Спасибо за ваш заказ!'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()