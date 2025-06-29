# Form Images
from io import BytesIO
from os import name
from PIL import Image
from django.core.files import File
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.db import models
from vendor.models import Vendor


# Create your models here.
class Brand(models.Model):
    name = models.CharField(_('Название'), max_length=100)
    slug = models.SlugField(_('URL-метка'), unique=True)
    description = models.TextField(_('Описание'), blank=True, null=True)
    logo = models.ImageField(_('Логотип'), upload_to='brand_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Бренд')
        verbose_name_plural = _('Бренды')

class Category(models.Model):
    title = models.CharField(_('Название'), max_length=50)
    slug = models.SlugField(_('URL-метка'), max_length=50)

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        ordering = ['title']
    
    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('Категория'), related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, verbose_name=_('Продавец'), related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, verbose_name=_('Бренд'), related_name='products', on_delete=models.SET_NULL, null=True)
    title = models.CharField(_('Название'), max_length=50)
    slug = models.SlugField(_('URL-метка'), max_length=50)
    description = models.TextField(_('Описание'), blank=True, null=True)
    price = models.DecimalField(_('Цена'), max_digits=19, decimal_places=2)
    is_popular = models.BooleanField(_('Популярный'), default=False)
    created_at = models.DateTimeField(_('Дата создания'), default=timezone.now)
    image = models.ImageField(_('Изображение'), upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(_('Миниатюра'), upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
    
    def __str__(self):
        return self.title
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'
    
    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img = img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        
        thumbnail = File(thumb_io, name=image.name)
        
        return thumbnail


