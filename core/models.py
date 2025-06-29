from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.

class Banner(models.Model):
    title = models.CharField(_('Title'), max_length=200)
    subtitle = models.CharField(_('Subtitle'), max_length=200, default='', blank=True)
    description = models.TextField(_('Description'), blank=True)
    image = models.ImageField(_('Image'), upload_to='banners/')
    link = models.URLField(_('Link'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    order = models.PositiveIntegerField(_('Order'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Список желаний')
        verbose_name_plural = _('Списки желаний')

    def __str__(self):
        if self.user:
            return f"Wishlist for {self.user.username}"
        return f"Anonymous Wishlist ({self.session_key})"
