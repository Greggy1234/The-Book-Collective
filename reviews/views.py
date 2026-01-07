from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Review, Rating
from status.models import Status


# Create your views here.
def recent_reviews(request):
    """
    Docstring for recent_reviews

    :param request: Description
    """
    review = Review.objects.select_related("object", "author").order_by("-created_on")[:8]
    rating = Rating.objects.select_related("object", "author").order_by("-created_on")
    book_status = Status.objects.select_related("object", "author").order_by("-created_on")

    return render(
        request,
        "review/index.html",
        {
            "review": review,
            "rating": rating,
            "book_status": book_status,
        }
    )
 

def all_reviews(request):
    """
    Docstring for recent_reviews

    :param request: Description
    """
    review = Review.objects.select_related("object", "author").order_by("-created_on")
    rating = Rating.objects.select_related("object", "author").order_by("-created_on")

    review_paginator = Paginator(review, 20)
    review_page_number = request.Get.get("page")
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
    Docstring for review_detail

    :param request: Description
    :param slug: Description
    """
    review = get_object_or_404(Review, slug=slug)
    rating = Rating.objects.all().filter(author=request.user, object=review.object)

    return render(
        request,
        "review/review-detail.html",
        {
            "review": review,
            "rating": rating
        }
    )
