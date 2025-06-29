from django.core.management.base import BaseCommand
from product.models import Product
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check media files status'

    def handle(self, *args, **options):
        # Check if media root exists
        self.stdout.write(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
        self.stdout.write(f"MEDIA_ROOT exists: {os.path.exists(settings.MEDIA_ROOT)}")
        
        # List all files in uploads directory
        uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        self.stdout.write(f"\nFiles in uploads directory:")
        if os.path.exists(uploads_dir):
            for file in os.listdir(uploads_dir):
                if file != '.DS_Store':
                    self.stdout.write(f"- {file}")
        
        # Check all products
        products = Product.objects.all()
        self.stdout.write(f"\nAll products ({products.count()}):")
        
        for product in products:
            self.stdout.write(f"\nProduct: {product.title}")
            self.stdout.write(f"Image field value: '{product.image}'")
            if product.image:
                image_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
                self.stdout.write(f"Image path: {image_path}")
                self.stdout.write(f"Image exists: {os.path.exists(image_path)}")
            if product.thumbnail:
                self.stdout.write(f"Thumbnail field value: '{product.thumbnail}'")
                thumb_path = os.path.join(settings.MEDIA_ROOT, str(product.thumbnail))
                self.stdout.write(f"Thumbnail path: {thumb_path}")
                self.stdout.write(f"Thumbnail exists: {os.path.exists(thumb_path)}") 