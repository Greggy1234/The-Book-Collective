from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from django.contrib.auth.models import User
from .models import Status
from reviews.models import Rating


# Create your views here.
def profile_page(request, username):
    """
    Docstring for profile_page

    :param request: Description
    """
    profile = get_object_or_404(User, username=username)
    book_status = Status.objects.select_related("object", "author").filter(author=profile).order_by("-created_on")
    book_read_count = Status.objects.filter(author=profile, status=3).count()
    user_avg_rating = Rating.objects.filter(author=profile).aggregate(Avg('rating'))['rating__avg']

    return render(
        request,
        "status/profile.html",
        {
            "book_status": book_status,
            "book_read_count": book_read_count,
            "profile": profile,
            "avg_rating": user_avg_rating,
        }
    )


def books_read(request, username):
    """
    Docstring for books_currently_reading

    :param request: Description
    """
    profile = get_object_or_404(User, username=username)
    books_read = Status.objects.select_related("object", "author").filter(author=profile, status=3).order_by("-created_on")

    return render(
        request,
        "status/book_read.html",
        {
            "books_read": books_read,
            "profile": profile,
        }
    )


def books_wishlist(request, username):
    """
    Docstring for books_currently_reading

    :param request: Description
    """
    profile = get_object_or_404(User, username=username)
    books_wish = Status.objects.select_related("object", "author").filter(author=profile, status=1).order_by("-created_on")

    return render(
        request,
        "status/book_wish.html",
        {
            "books_wish": books_wish,
            "profile": profile,
        }
    )
