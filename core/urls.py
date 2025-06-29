from django.urls import path
from . import views

app_name = 'core'


urlpatterns = [
    path('', views.frontpage, name="home"),
    path('contact-us/', views.contactpage, name="contact"),
    path('register/', views.register, name="register"),
    path('account/', views.account, name='account'),
    path('toggle-wishlist/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]
