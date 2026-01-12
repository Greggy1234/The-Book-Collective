from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Review, Rating
from status.models import Status


# Create your views here.
def recent_reviews(request):
    """
    Renders the most recent 8 reviews in :model:`reviews.Review
    with all objects in :model:`reviews.Rating`
    and all objects in :model:`status.Status`

    **Context**
    ``review``
        Most recent 4 instances of :model:`reviews.Review`
    ``rating``
        All instances of :model:`reviews.Rating`
    ``book_status_currently_reading``
        Most recent 4 :model:`status.Status` where status is currently reading
    ``book_status_wishlist``
        Most recent 4 :model:`status.Status` where status is wishlist

    **Template**
        :template:`review/index.html`
    """
    review = Review.objects.select_related("object", "author").order_by("-created_on")[:4]
    rating = Rating.objects.select_related("object", "author").order_by("-created_on")
    book_status_currently_reading = Status.objects.select_related("object", "author").filter(status=2, author=request.user).order_by("-updated_on")[:4]
    book_status_wishlist = Status.objects.select_related("object", "author").filter(status=1, author=request.user).order_by("-updated_on")[:4]

    return render(
        request,
        "review/index.html",
        {
            "review": review,
            "rating": rating,
            "book_status_currently_reading": book_status_currently_reading,
            "book_status_wishlist": book_status_wishlist,
        }
    )


def all_reviews(request):
    """
    Renders all reviews in :model:`reviews.Review
    with all objects in :model:`reviews.Rating`.
    Paginated for 15 reviews per page

    **Context**
    ``review``
        All instances of :model:`reviews.Review`
    ``rating``
        All instances of :model:`reviews.Rating`

    **Template**
        :template:`review/all-reviews.html`
    """
    review = Review.objects.select_related("object", "author").order_by("-created_on")
    rating = Rating.objects.select_related("object", "author").order_by("-created_on")

    review_paginator = Paginator(review, 15)
    review_page_number = request.GET.get("page")
    review_page_obj = review_paginator.get_page(review_page_number)

    return render(
        request,
        "review/all-reviews.html",
        {
            "review": review_page_obj,
            "rating": rating,
        }
    )


def review_detail(request, slug):
    """
    Displays an individual :model:`reviews.Review`

    **Context**
    ``review``
        An instance of :model:`reviews.Review`
    ``rating``
        All instances of :model:`reviews.Rating` related to review

    **Template**
        :template:`review/review-detail.html`
    """
    review = get_object_or_404(Review, slug=slug)
    rating = Rating.objects.all().filter(author=review.author, object=review.object).first()

    return render(
        request,
        "review/review-detail.html",
        {
            "review": review,
            "rating": rating
        }
    )
