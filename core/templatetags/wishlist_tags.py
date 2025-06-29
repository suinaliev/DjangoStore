from django import template
from django.template.defaultfilters import register
from core.models import Wishlist

register = template.Library()

@register.filter(name='wishlist_by_session')
def wishlist_by_session(session_key):
    """
    Get wishlist by session key for anonymous users
    """
    try:
        # Get all wishlists for this session
        session_wishlists = Wishlist.objects.filter(session_key=session_key)
        
        if session_wishlists.count() > 1:
            # If multiple wishlists exist, merge them into one
            wishlist = session_wishlists.first()
            for other_wishlist in session_wishlists[1:]:
                wishlist.products.add(*other_wishlist.products.all())
                other_wishlist.delete()
            return wishlist
        else:
            return session_wishlists.first()
    except Exception:
        return None

@register.simple_tag(takes_context=True)
def get_wishlist_count(context):
    """
    Get the count of items in the wishlist for both authenticated and anonymous users
    """
    request = context['request']
    if request.user.is_authenticated:
        try:
            # Get all wishlists for this user
            user_wishlists = request.user.wishlist_set.all()
            if user_wishlists.count() > 1:
                # Merge multiple wishlists
                wishlist = user_wishlists.first()
                for other_wishlist in user_wishlists[1:]:
                    wishlist.products.add(*other_wishlist.products.all())
                    other_wishlist.delete()
                return wishlist.products.count()
            elif user_wishlists.exists():
                return user_wishlists.first().products.count()
            return 0
        except AttributeError:
            return 0
    else:
        try:
            # Get all wishlists for this session
            session_wishlists = Wishlist.objects.filter(session_key=request.session.session_key)
            if session_wishlists.count() > 1:
                # Merge multiple wishlists
                wishlist = session_wishlists.first()
                for other_wishlist in session_wishlists[1:]:
                    wishlist.products.add(*other_wishlist.products.all())
                    other_wishlist.delete()
                return wishlist.products.count()
            elif session_wishlists.exists():
                return session_wishlists.first().products.count()
            return 0
        except Exception:
            return 0 