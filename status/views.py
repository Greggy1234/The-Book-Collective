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
    Docstring for profile_page

    :param request: Description
    """
    user = get_object_or_404(User, username=username)
    book_status = Status.objects.select_related("object", "author").filter(author=user).order_by("-created_on")
    book_status_wishlist = book_status.filter(status=1)[:4]
    book_status_reading = book_status.filter(status=2)
    book_status_read = book_status.filter(status=3)[:4]
    book_status_dnf = book_status.filter(status=4)[:4]
    book_read_count = Status.objects.filter(author=user, status=3).count()
    user_avg_rating = Rating.objects.filter(author=user).aggregate(Avg('rating'))['rating__avg']

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
            "avg_rating": user_avg_rating,
        }
    )


def books_read(request, username):
    """
    Docstring for books_currently_reading

    :param request: Description
    """
    user = get_object_or_404(User, username=username)
    book_status = Status.objects.select_related("object", "author").filter(author=user, status=3).order_by("-created_on")
    books_read = book_status.filter(status=3)

    books_read_paginator = Paginator(books_read, 12)
    books_read_page_number = request.Get.get("page")
    books_read_page_obj = books_read_paginator.get_page(books_read_page_number)

    return render(
        request,
        "status/book-read.html",
        {
            "books_read": books_read,
            "books_read_page_obj": books_read_page_obj,
            "user": user,
        }
    )


def books_wishlist(request, username):
    """
    Docstring for books_currently_reading

    :param request: Description
    """
    user = get_object_or_404(User, username=username)
    book_status = Status.objects.select_related("object", "author").filter(author=user, status=3).order_by("-created_on")
    books_wish = book_status.filter(status=1)

    books_wish_paginator = Paginator(books_wish, 12)
    books_wish_page_number = request.Get.get("page")
    books_wish_page_obj = books_wish_paginator.get_page(books_wish_page_number)

    return render(
        request,
        "status/wishlist.html",
        {
            "books_wish": books_wish,
            "books_wish_page_obj": books_wish_page_obj,
            "user": user,
        }
    )


def add_to_wishlist(request, slug):
    """
    Docstring for add_to_wishlist

    :param request: Description
    :param slug: Description
    """
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST":
        status, created = Status.get_or_create(
            object=book,
            author=request.User,
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


def add_to_currently_reading(request, slug):
    """
    Docstring for add_to_currently_reading
    
    :param request: Description
    :param slug: Description
    """
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST":
        status, created = Status.get_or_create(
            object=book,
            author=request.User,
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


def add_to_read(request, slug):
    """
    Docstring for add_to_read
    
    :param request: Description
    :param slug: Description
    """
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST":
        status, created = Status.get_or_create(
            object=book,
            author=request.User,
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


def add_to_dnf(request, slug):
    """
    Docstring for add_to_dnf
    
    :param request: Description
    :param slug: Description
    """
    book = get_object_or_404(Book, slug=slug)
    if request.method == "POST":
        status, created = Status.get_or_create(
            object=book,
            author=request.User,
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


def delete_status(request, slug):
    """
    Docstring for delete_status
    
    :param request: Description
    """
    book = get_object_or_404(Book, slug=slug)
    status = get_object_or_404(Status, object=book, author=request.user)
    if request == "POST":
        if status.author == request.user:
            status.delete()
    
    return HttpResponseRedirect(reverse('book_detail', args=[slug]))
