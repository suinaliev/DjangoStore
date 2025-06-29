import stripe #pip install stripe 

from django. conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .cart import Cart
from .forms import CheckoutForm
from product.models import Product

from order.utilities import checkout, notify_vendor, notify_customer

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product_id=product_id, quantity=quantity, update_quantity=False)
        messages.success(request, "Товар добавлен в корзину")
        
    return redirect('product:product', category_slug=product.category.slug, product_slug=product.slug)

# Create your views here.
def cart_detail(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        if len(cart) == 0:
            messages.warning(request, 'Ваша корзина пуста')
            return redirect('cart:cart')
        return redirect('order:checkout')
    
    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart:cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart:cart')
        
    return render(request, 'cart/cart.html', {'cart': cart})


def success(request):
    return render(request, 'cart/success.html')