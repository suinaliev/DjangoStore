from django.urls import path
from . import views


app_name = 'order'


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('thank-you/<int:order_id>/', views.thank_you, name='thank_you'),
]
