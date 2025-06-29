from django import forms
from .models import Order, ShippingMethod, PaymentMethod

class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Пожалуйста, введите ваше имя'}
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Пожалуйста, введите вашу фамилию'}
    )
    email = forms.EmailField(
        max_length=100,
        required=True,
        error_messages={'required': 'Пожалуйста, введите ваш email'}
    )
    phone = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Пожалуйста, введите ваш телефон'}
    )
    address = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Пожалуйста, введите адрес доставки'}
    )
    zipcode = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Пожалуйста, введите почтовый индекс'}
    )
    place = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Пожалуйста, введите город'}
    )
    
    shipping_method = forms.ModelChoiceField(
        queryset=ShippingMethod.objects.filter(is_active=True),
        empty_label=None,
        required=True,
        error_messages={'required': 'Пожалуйста, выберите способ доставки'},
        label='Способ доставки',
        widget=forms.RadioSelect(attrs={'class': 'shipping-radio'})
    )
    
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.filter(is_active=True),
        empty_label=None,
        required=True,
        error_messages={'required': 'Пожалуйста, выберите способ оплаты'},
        label='Способ оплаты',
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'})
    )
    
    stripe_token = forms.CharField(required=False, widget=forms.HiddenInput)
    
    class Meta:
        model = Order
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'phone', 
            'address', 
            'zipcode', 
            'place', 
            'shipping_method', 
            'payment_method', 
            'stripe_token'
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'address': 'Адрес',
            'zipcode': 'Индекс',
            'place': 'Город'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Добавляем классы Bootstrap и плейсхолдеры
        for field_name, field in self.fields.items():
            if field_name not in ['shipping_method', 'payment_method', 'stripe_token']:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label,
                    'required': 'required'  # Добавляем HTML5 required атрибут
                })
        
        # Добавляем цены в data-атрибуты для методов доставки
        for radio in self.fields['shipping_method'].widget.choices:
            if hasattr(radio[1], 'price'):
                radio[1].attrs = {'data-price': radio[1].price}
                
        # Добавляем data-type для методов оплаты
        for radio in self.fields['payment_method'].widget.choices:
            if hasattr(radio[1], 'payment_type'):
                radio[1].attrs = {
                    'data-type': radio[1].payment_type,
                    'class': 'payment-radio'
                }
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        stripe_token = cleaned_data.get('stripe_token')
        
        if payment_method and payment_method.payment_type == 'stripe' and not stripe_token:
            raise forms.ValidationError({
                'payment_method': 'При оплате картой необходимо ввести данные карты'
            }) 