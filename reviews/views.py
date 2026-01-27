from django.shortcuts import render, get_object_or_404, reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Review, Rating, Like
from .forms import RatingForm, ReviewForm
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
    for rev in review:
        rev.user_review_like = rev.review_like.filter(author=request.user).first()
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
    for rev in review:
        rev.user_review_like = rev.review_like.filter(author=request.user).first()
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
    ``add_rating_form``
        An instance of :form:`reviews.RatingForm`
    ``add_rating_form_modal``
        An instance of :form:`reviews.RatingForm` to be used in the modal
    ``add_review_form``
        An instance of :form:`reviews.ReviewForm`
    ``review``
        An instance of :model:`reviews.Review`
    ``rating``
        All instances of :model:`reviews.Rating` related to review
    ``user_review_like``
        Returns if the request.user has liked the review

    **Template**
        :template:`review/review-detail.html`
    """
    review = get_object_or_404(Review, slug=slug)
    user_review_like = review.review_like.filter(author=request.user).first()
    rating = Rating.objects.all().filter(author=review.author, object=review.object).first()

    add_rating_form = RatingForm()
    add_review_form = ReviewForm()
    add_rating_form_modal = RatingForm(prefix='modal')

    return render(
        request,
        "review/review-detail.html",
        {
            "add_rating_form": add_rating_form,
            "add_rating_form_modal": add_rating_form_modal,
            "add_review_form": add_review_form,
            "review": review,
            "rating": rating,
            "user_review_like": user_review_like
        }
    )


def add_review_like(request, slug):
    '''
    Adds a users like for a specific review to :model:`reviews.Like`

    **Context**
    ``review``
        An instance of :model:`review.Review`
    ``book_slug``
        The slug of the book connected to the review
    '''
    review = get_object_or_404(Review, slug=slug)
    book_slug = review.object.slug
    if request.method == "POST":
        Like.objects.create(object=review, author=request.user)
        messages.add_message(request, messages.SUCCESS, f"You've successfully liked {review}")
    else:
        messages.add_message(request, messages.ERROR, f'There was a problem liking {review}')

    if '/books/' in request.META['HTTP_REFERER']:
        return HttpResponseRedirect(reverse('book_detail', args=[book_slug]))
    elif request.META['HTTP_REFERER'].endswith('reviews/'):
        return HttpResponseRedirect(reverse('all_reviews'))
    elif '/reviews/' in request.META['HTTP_REFERER']:
        return HttpResponseRedirect(reverse('review_detail', args=[slug]))
    else:
        return HttpResponseRedirect(reverse('homepage'))


def delete_review_like(request, slug):
    '''
    Deletes a users like for a specific review to :model:`reviews.Like`

    **Context**
    ``review``
        An instance of :model:`review.Review`
    ``book_slug``
        The slug of the book connected to the review
    ``like``
        an instance of :mode:`reviews.Like`
    '''
    review = get_object_or_404(Review, slug=slug)
    book_slug = review.object.slug
    like = get_object_or_404(Like, object=review, author=request.user)
    if request.method == "POST":
        if like.author == request.user:
            like.delete()
            messages.add_message(request, messages.SUCCESS, "Your like has been removed")
    else:
        messages.add_message(request, messages.ERROR, 'There was a problem removing your like')

    if '/books/' in request.META['HTTP_REFERER']:
        return HttpResponseRedirect(reverse('book_detail', args=[book_slug]))
    elif request.META['HTTP_REFERER'].endswith('reviews/'):
        return HttpResponseRedirect(reverse('all_reviews'))
    elif '/reviews/' in request.META['HTTP_REFERER']:
        return HttpResponseRedirect(reverse('review_detail', args=[slug]))
    else:
        return HttpResponseRedirect(reverse('homepage'))
