from django.shortcuts import render, get_object_or_404, reverse
from django.db.models import Avg
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Status
from reviews.models import Rating
from book.models import Book


# Create your views here.
def profile_page(request, username):
    """
    Renders a user's profile taken from :model:`auth.User` and 
    showing the status of books from that user from :model:`status.Status`
    with specifics to only show the most recent 4 book statuses.
    It includes the amount of books read and the users average rating
    
    **Context**
    ``book_status``
        All instances of :model:`status.Status` relating to the user
    ``book_read_count``
        A count of how many books the user has of status=3
    ``book_status_wishlist``
        The 4 most recent books from the user with status=1
    ``book_status_reading``
        The 4 most recent books from the user with status=2
    ``book_status_read``
        The 4 most recent books from the user with status=3
    ``book_read_dnf``
        The 4 most recent books from the user with status=4
    ``user``
        An instance of :model:`auth.User`
    ``avg_rating``
        The average rating of all books from the user takend from
        :model:`reviews.Rating`

    **Template**
        :template:`status/profile.html`
    """
    user = get_object_or_404(User, username=username)
    book_status = Status.objects.select_related("object", "author").filter(author=user).order_by("-created_on")
    book_status_wishlist = book_status.filter(status=1).order_by("-updated_on")[:4]
    book_status_reading = book_status.filter(status=2).order_by("-updated_on")[:4]
    book_status_read = book_status.filter(status=3).order_by("-updated_on")[:4]
    book_status_dnf = book_status.filter(status=4).order_by("-updated_on")[:4]
    book_read_count = Status.objects.filter(author=user, status=3).count()

    get_ratings = Rating.objects.filter(author=user)
    avg_rating = get_ratings.aggregate(Avg('rating'))['rating__avg']
    if not avg_rating:
        user_avg_rating = None
    else:
        user_avg_rating = round(avg_rating, 2)

    return render(
        request,
        "status/profile.html",
        {
            "book_status": book_status,
            "book_read_count": book_read_count,
            "book_status_wishlist": book_status_wishlist,
            "book_status_reading": book_status_reading,
            "book_status_read": book_status_read,
            "book_read_dnf": book_status_dnf,
            "user": user,
            "user_avg_rating": user_avg_rating,
        }
    )


def books_read(request, username):
    """
    Renders all the books a user has read from :model:`status.Status`,
    paginated to show 12 per page

    **Context**
    ``books_read_page_obj``
        All instances of :model:`status.Status` where status=3
        relating to the user
    ``user``
        An instance of :model:`auth.User`
    """
    user = get_object_or_404(User, username=username)
    book_status = Status.objects.select_related("object", "author").filter(author=user).order_by("-created_on")
    books_read = book_status.filter(status=3)

    books_read_paginator = Paginator(books_read, 12)
    books_read_page_number = request.GET.get("page")
    books_read_page_obj = books_read_paginator.get_page(books_read_page_number)

    return render(
        request,
        "status/book-read.html",
        {
            "books_read_page_obj": books_read_page_obj,
            "user": user,
        }
    )


def books_wishlist(request, username):
    """
    Renders all the books a user has on their wishlist from :model:`status.Status`,
    paginated to show 12 per page

    **Context**
    ``books_wish_page_obj``
        All instances of :model:`status.Status` where status=1
        relating to the user
    ``user``
        An instance of :model:`auth.User`
    """
    user = get_object_or_404(User, username=username)
    book_status = Status.objects.select_related("object", "author").filter(author=user).order_by("-created_on")
    books_wish = book_status.filter(status=1)

    books_wish_paginator = Paginator(books_wish, 12)
    books_wish_page_number = request.GET.get("page")
    books_wish_page_obj = books_wish_paginator.get_page(books_wish_page_number)

    return render(
        request,
        "status/wishlist.html",
        {
            "books_wish_page_obj": books_wish_page_obj,
            "user": user,
        }
    )


def add_to_wishlist(request, username, slug):
    """
    Adds a book to the users wishlist

    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``status``
        An instance of :model:`status.Status`
    """
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST":
        status, created = Status.objects.get_or_create(
            object=book,
            author=request.user,
            defaults={'status': 1}
        )
        if created:
            messages.add_message(
                request, messages.SUCCESS,
                f'{book.title} added to wishlist'
            )
        else:
            status.status = 1
            status.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'{book.title} added to wishlist'
            )    

    return HttpResponseRedirect(reverse('book_detail', args=[slug]))


def add_to_currently_reading(request, username,slug):
    """
    Adds a book to the users currently reading list

    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``status``
        An instance of :model:`status.Status`
    """
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST":
        status, created = Status.objects.get_or_create(
            object=book,
            author=request.user,
            defaults={'status': 2}
        )
        if created:
            messages.add_message(
                request, messages.SUCCESS,
                f'{book.title} added to currently reading'
            )
        else:
            status.status = 2
            status.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'{book.title} added to currently reading'
            )    

    return HttpResponseRedirect(reverse('book_detail', args=[slug]))


def add_to_read(request, username, slug):
    """
    Adds a book to the users read list

    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``status``
        An instance of :model:`status.Status`
    """
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST":
        status, created = Status.objects.get_or_create(
            object=book,
            author=request.user,
            defaults={'status': 3}
        )
        if created:
            messages.add_message(
                request, messages.SUCCESS,
                f'{book.title} added to read books'
            )
        else:
            status.status = 3
            status.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'{book.title} added to read books'
            )    

    return HttpResponseRedirect(reverse('book_detail', args=[slug]))


def add_to_dnf(request, username, slug):
    """
    Adds a book to the users dnf list

    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``status``
        An instance of :model:`status.Status`
    """
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST":
        status, created = Status.objects.get_or_create(
            object=book,
            author=request.user,
            defaults={'status': 4}
        )
        if created:
            messages.add_message(
                request, messages.SUCCESS,
                f'{book.title} added to DNF pile'
            )
        else:
            status.status = 4
            status.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'{book.title} added to DNF pile'
            )    

    return HttpResponseRedirect(reverse('book_detail', args=[slug]))


def delete_status(request, username, slug):
    """
    Deletes the user's status from that book
    irrespective of which status it was

    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``status``
        An instance of :model:`status.Status`
    """
    book = get_object_or_404(Book, slug=slug)
    status = get_object_or_404(Status, object=book, author=request.user)
    status_name = status.get_status_display()
    if request.method == "POST":
        if status.author == request.user:
            status.delete()
            messages.add_message(
                request, messages.SUCCESS,
                f'{book.title} has been removed from {status_name}'
            )

    return HttpResponseRedirect(reverse('book_detail', args=[slug]))
