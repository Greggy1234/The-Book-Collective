from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Book


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
