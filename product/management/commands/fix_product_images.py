from django.core.management.base import BaseCommand
from product.models import Product
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Fix product images by associating available files'

    def handle(self, *args, **options):
        # Get list of available images
        uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        available_images = []
        if os.path.exists(uploads_dir):
            for file in os.listdir(uploads_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) and file != '.DS_Store':
                    available_images.append(file)
        
        self.stdout.write(f"Found {len(available_images)} available images")
        
        # Get products without images
        products = Product.objects.filter(image='')
        self.stdout.write(f"Found {products.count()} products without images")
        
        # Associate images with products
        for i, product in enumerate(products):
            if i < len(available_images):
                image_name = available_images[i]
                product.image = f'uploads/{image_name}'
                product.save()
                self.stdout.write(f"Associated {image_name} with {product.title}")
                
                # Generate thumbnail
                product.thumbnail = product.make_thumbnail(product.image)
                product.save()
                self.stdout.write(f"Generated thumbnail for {product.title}")
            else:
                self.stdout.write(f"No more images available for {product.title}")
        
        self.stdout.write(self.style.SUCCESS('Successfully fixed product images')) 