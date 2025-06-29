import stripe
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from cart.cart import Cart
from .forms import OrderForm
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        print("POST data:", request.POST)  # Debug print
        print("Form errors:", form.errors)  # Debug print
        
        if form.is_valid():
            try:
                order = form.save(commit=False)
                # Only set user if authenticated
                if request.user.is_authenticated:
                    order.user = request.user
                
                # Рассчитываем общую стоимость
                total_cost = cart.get_total_cost()
                if order.shipping_method:
                    total_cost += order.shipping_method.price
                
                order.paid_amount = total_cost
                
                # Обработка оплаты в зависимости от метода
                if order.payment_method.payment_type == 'stripe':
                    try:
                        # Создаем платеж в Stripe
                        charge = stripe.Charge.create(
                            amount=int(total_cost * 100),  # Конвертируем в копейки
                            currency='rub',
                            description=f'Заказ {order.first_name} {order.last_name}',
                            source=form.cleaned_data['stripe_token']
                        )
                        
                        if charge.paid:
                            order.paid = True
                            messages.success(request, 'Оплата прошла успешно!')
                        else:
                            messages.error(request, 'Ошибка при обработке платежа')
                            return redirect('order:checkout')
                            
                    except stripe.error.CardError as e:
                        messages.error(request, f'Ошибка карты: {e.error.message}')
                        return redirect('order:checkout')
                    except stripe.error.StripeError as e:
                        messages.error(request, 'Произошла ошибка при обработке платежа')
                        return redirect('order:checkout')
                
                elif order.payment_method.payment_type == 'bank_transfer':
                    # Отправляем email с реквизитами
                    context = {
                        'order': order,
                        'total_cost': total_cost,
                        'bank_details': {
                            'bank_name': 'Сбербанк',
                            'account_number': '40817810099910004312',
                            'bik': '044525225',
                            'correspondent_account': '30101810400000000225'
                        }
                    }
                    
                    message = render_to_string('order/email/bank_transfer.html', context)
                    send_mail(
                        'Реквизиты для оплаты заказа',
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [order.email],
                        html_message=message
                    )
                    messages.info(request, 'Реквизиты для оплаты отправлены на ваш email')
                
                elif order.payment_method.payment_type == 'cash':
                    messages.info(request, 'Оплата будет произведена наличными при получении')
                
                # Сохраняем заказ
                order.save()
                
                # Создаем элементы заказа
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        vendor=item['product'].vendor,
                        price=item['price'],
                        quantity=item['quantity']
                    )
                
                # Очищаем корзину
                cart.clear()
                
                # Отправляем подтверждение заказа
                context = {
                    'order': order,
                    'items': OrderItem.objects.filter(order=order),
                    'total_cost': total_cost
                }
                
                confirmation_message = render_to_string('order/email/order_confirmation.html', context)
                send_mail(
                    'Подтверждение заказа',
                    confirmation_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [order.email],
                    html_message=confirmation_message
                )
                
                messages.success(request, 'Заказ успешно оформлен!')
                return redirect('order:thank_you', order_id=order.id)
                
            except Exception as e:
                print("Error:", str(e))  # Debug print
                messages.error(request, 'Произошла ошибка при оформлении заказа')
                return redirect('order:checkout')
    else:
        # Предзаполняем форму данными пользователя только если он авторизован
        initial_data = {}
        if request.user.is_authenticated:
            if request.user.first_name:
                initial_data['first_name'] = request.user.first_name
            if request.user.last_name:
                initial_data['last_name'] = request.user.last_name
            if request.user.email:
                initial_data['email'] = request.user.email
            
        form = OrderForm(initial=initial_data)
    
    return render(request, 'order/checkout.html', {
        'form': form,
        'cart': cart,
        'stripe_pub_key': settings.STRIPE_PUB_KEY
    })

def thank_you(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/thank_you.html', {
        'order': order
    })
