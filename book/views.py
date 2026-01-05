from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from .models import Book
from .forms import AddBook


# Create your views here.
class book_overview(ListView):
    """
    Docstring for book_overview

    :param request: Description
    """
    model = Book
    template_name = "book/books.html"
    context_object_name = "books"
    paginate_by = 10


def book_detail(request, slug):
    """
    Docstring for book_detail

    :param request: Description
    """
    book = get_object_or_404(Book, slug=slug)
    review = book.book_review.all().order_by("-created_on")

    return render(
        request,
        "books/books_detail.html",
        {
            "book": book,
            "review": review,
        }
    )


def add_book(request):
    """
    """
    if request.method == "POST":
        add_book_form = AddBook(data=request.POST)
        if add_book_form.is_valid():
            book = add_book_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'{book.title} has been saved. Thank you for adding more books to the site!'
            )

    add_book_form = AddBook()

    return render(
        request,
        "books/add_book.html",
        {
            "add_book_form": add_book_form
        }
    )
