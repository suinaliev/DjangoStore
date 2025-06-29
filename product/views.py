import random # To get random products from the database
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from .models import Category, Product, Brand

from django.db.models import Q

from .forms import AddToCartForm
from cart.cart import Cart
from django.core.paginator import Paginator


# Create your views here.
def product(request, category_slug, product_slug):
    # Create instance of Cart class
    cart = Cart(request)

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    # Check whether the AddToCart button is clicked or not
    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)

            messages.success(request, "The product was added to the cart.")

            return redirect('product:product', category_slug=category_slug, product_slug=product_slug)            
    
    else:
        form = AddToCartForm()

    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[0:4]

    context = {
        'product': product,
        'similar_products': similar_products,
        'form': form,
    }

    return render(request, 'product/product.html', context)


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request,'product/category.html', {'category': category})


def search(request):
    query = request.GET.get('query', '') # second is default parameter which is empty
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'product/search.html', {'products':products, 'query': query})

def catalog(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    # Фильтрация по категориям
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        products = products.filter(category__slug__in=selected_categories)
    
    # Фильтрация по брендам
    selected_brands = request.GET.getlist('brand')
    if selected_brands:
        products = products.filter(brand__id__in=selected_brands)
    
    # Фильтрация по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Сортировка
    sort = request.GET.get('sort', 'popular')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    else:  # popular
        products = products.filter(is_popular=True) | products.all()
    
    # Пагинация
    paginator = Paginator(products, 12)  # 12 товаров на странице
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    # Проверка наличия активных фильтров
    has_filters = bool(selected_categories or selected_brands or min_price or max_price)
    
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'selected_categories': selected_categories,
        'selected_brands': selected_brands,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
        'has_filters': has_filters
    }
    
    return render(request, 'product/catalog.html', context)