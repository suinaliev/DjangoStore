from django.shortcuts import render, redirect, get_object_or_404
from .models import Banner, Wishlist
from product.models import Product, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from order.models import Order
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _

# Create your views here.

def frontpage(request):
    banners = Banner.objects.filter(is_active=True)
    categories = Category.objects.all()
    popular_products = Product.objects.filter(is_popular=True)[:8]  # Показываем 8 популярных товаров
    
    # Handle wishlists
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        # Clean up any session-based wishlists
        if request.session.session_key:
            Wishlist.objects.filter(session_key=request.session.session_key).delete()
    else:
        if request.session.session_key:
            session_wishlists = Wishlist.objects.filter(session_key=request.session.session_key)
            if session_wishlists.count() > 1:
                # Merge multiple wishlists into one
                wishlist = session_wishlists.first()
                for other_wishlist in session_wishlists[1:]:
                    wishlist.products.add(*other_wishlist.products.all())
                    other_wishlist.delete()
    
    context = {
        'banners': banners,
        'categories': categories,
        'popular_products': popular_products,
    }
    
    return render(request, 'core/frontpage.html', context)


def contactpage(request):
    return render(request, 'core/contact.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Handle wishlist merging
            session_key = request.session.session_key
            if session_key:
                # Get all session wishlists
                session_wishlists = Wishlist.objects.filter(session_key=session_key)
                if session_wishlists.exists():
                    # Create user wishlist
                    user_wishlist, created = Wishlist.objects.get_or_create(user=user)
                    
                    # Merge all session wishlists into user wishlist
                    for session_wishlist in session_wishlists:
                        user_wishlist.products.add(*session_wishlist.products.all())
                        session_wishlist.delete()
            
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def account(request):
    # Получаем заказы текущего пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    return render(request, 'core/account.html', {
        'title': 'Личный кабинет',
        'orders': orders,
        'wishlist': wishlist
    })

@require_http_methods(["POST"])
def toggle_wishlist(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        
        if request.user.is_authenticated:
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            # Clean up any session-based wishlists
            if request.session.session_key:
                Wishlist.objects.filter(session_key=request.session.session_key).delete()
        else:
            if not request.session.session_key:
                request.session.create()
                
            # Get or create a single wishlist for this session
            session_wishlists = Wishlist.objects.filter(session_key=request.session.session_key)
            if session_wishlists.exists():
                wishlist = session_wishlists.first()
                # Clean up any additional wishlists
                for other_wishlist in session_wishlists[1:]:
                    wishlist.products.add(*other_wishlist.products.all())
                    other_wishlist.delete()
            else:
                wishlist = Wishlist.objects.create(session_key=request.session.session_key)
        
        if product in wishlist.products.all():
            wishlist.products.remove(product)
            is_in_wishlist = False
            message = _("Товар удален из списка желаний")
        else:
            wishlist.products.add(product)
            is_in_wishlist = True
            message = _("Товар добавлен в список желаний")
        
        return JsonResponse({
            'status': 'success',
            'is_in_wishlist': is_in_wishlist,
            'message': message
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def wishlist_view(request):
    if request.user.is_authenticated:
        # For authenticated users, get or create a single wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        # Clean up any session-based wishlists if they exist
        if request.session.session_key:
            Wishlist.objects.filter(session_key=request.session.session_key).delete()
    else:
        # For anonymous users
        if not request.session.session_key:
            request.session.create()
            
        # Get all wishlists for this session
        session_wishlists = Wishlist.objects.filter(session_key=request.session.session_key)
        
        if session_wishlists.count() > 1:
            # If multiple wishlists exist, merge them into one
            wishlist = session_wishlists.first()
            for other_wishlist in session_wishlists[1:]:
                # Add products from other wishlists to the first one
                wishlist.products.add(*other_wishlist.products.all())
                other_wishlist.delete()
        elif session_wishlists.exists():
            wishlist = session_wishlists.first()
        else:
            # Create new wishlist if none exists
            wishlist = Wishlist.objects.create(session_key=request.session.session_key)
    
    return render(request, 'core/wishlist.html', {
        'wishlist': wishlist
    })