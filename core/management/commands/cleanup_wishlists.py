from django.core.management.base import BaseCommand
from core.models import Wishlist
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

class Command(BaseCommand):
    help = 'Clean up duplicate wishlists'

    def handle(self, *args, **kwargs):
        # Clean up user wishlists
        users_with_multiple_wishlists = User.objects.annotate(
            wishlist_count=Count('wishlist')
        ).filter(wishlist_count__gt=1)

        for user in users_with_multiple_wishlists:
            wishlists = user.wishlist_set.all()
            main_wishlist = wishlists.first()
            for other_wishlist in wishlists[1:]:
                main_wishlist.products.add(*other_wishlist.products.all())
                other_wishlist.delete()
            self.stdout.write(f"Merged {wishlists.count()} wishlists for user {user.username}")

        # Clean up session wishlists
        session_keys_with_multiple_wishlists = Wishlist.objects.filter(
            session_key__isnull=False
        ).values('session_key').annotate(
            count=Count('id')
        ).filter(count__gt=1)

        for item in session_keys_with_multiple_wishlists:
            session_key = item['session_key']
            wishlists = Wishlist.objects.filter(session_key=session_key)
            main_wishlist = wishlists.first()
            for other_wishlist in wishlists[1:]:
                main_wishlist.products.add(*other_wishlist.products.all())
                other_wishlist.delete()
            self.stdout.write(f"Merged {item['count']} wishlists for session {session_key}")

        self.stdout.write(self.style.SUCCESS('Successfully cleaned up duplicate wishlists')) 