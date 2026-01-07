from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from .models import Book
from .forms import AddBook, AddAuthor
from reviews.models import Review, Rating
from reviews.forms import ReviewForm, RatingForm


# Create your views here.
class BookOverview(ListView):
    """
    Docstring for book_overview

    :param request: Description
    """
    model = Book
    template_name = "book/books.html"
    context_object_name = "books"
    paginate_by = 12


class BookSearch(ListView):
    """
    """
    model = Book
    template_name = "book/search.html"
    context_object_name = "book_search"
    paginate_by = 12

# function get_queryset was taken from https://testdriven.io/blog/django-search/
    def get_queryset(self):
        query = self.request.GET.get("q")
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__author__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q")
        return context


def book_detail(request, slug):
    """
    Docstring for book_detail

    :param request: Description
    """
    book = get_object_or_404(Book, slug=slug)
    review = book.book_review.all().order_by("-created_on")
    review_count = book.book_review.count()
    user_review = book.book_review.filter(object=book, author=request.user)
    user_rating = book.book_rating.filter(object=book, author=request.user)
    user_status = book.book_status.filter(object=book, author=request.user)

    return render(
        request,
        "book/book-detail.html",
        {
            "book": book,
            "review": review,
            "review_count": review_count,
            "user_review": user_review,
            "user_rating": user_rating,
            "user_status": user_status,
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
        "book/add-book.html",
        {
            "add_book_form": add_book_form
        }
    )


def add_author(request):
    """
    Docstring for add_author

    :param request: Description
    """
    if request.method == "POST":
        add_author_form = AddAuthor(data=request.POST)
        if add_author_form.is_valid():
            author = add_author_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'{author.author} has been saved!'
            )

    return HttpResponseRedirect(reverse('add_book'))


def add_review(request, slug):
    """
    Docstring for add_review

    :param request: Description
    :param slug: Description
    """
    if request.method == "POST":
        book = get_object_or_404(Book, slug=slug)
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.object = book
            review.author = request.user
            review.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'Thank you for you review of {book.title}'
            )

    return HttpResponseRedirect(reverse('book_detail', args=[slug]))


def add_rating(request, slug):
    """
    Docstring for add_rating

    :param request: Description
    :param slug: Description
    """
    if request.method == "POST":
        book = get_object_or_404(Book, slug=slug)
        rating_form = RatingForm(data=request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.object = book
            rating.author = request.user
            rating.save()
            messages.add_message(
                request, messages.SUCCESS,
                f'Thank you for you rating of {book.title}'
            )

    return HttpResponseRedirect(reverse('book_detail', args=[slug]))


def edit_review(request, slug):
    """
    Docstring for edit_review
    
    :param request: Description
    :param slug: Description
    """
    if request.method == "POST":
        book = get_object_or_404(Book, slug=slug)
        review = get_object_or_404(Review, object=book, author=request.user)
        review_form = ReviewForm(data=request.POST, instance=review)
        if review_form.is_valid() and review.author == request.user:
            review = review_form.save(commit=False)
            review.object = book
            review.save()
            messages.add_message(request, messages.SUCCESS, f'Your review for {book.title} has been saved!')
        else:
            messages.add_message(request, messages.ERROR, 'There was an error updating your review')

    return HttpResponseRedirect(reverse('book_detail', args=[slug]))


def edit_rating(request, slug):
    """
    Docstring for edit_review

    :param request: Description
    :param slug: Description
    """
    if request.method == "POST":
        book = get_object_or_404(Book, slug=slug)
        rating = get_object_or_404(Rating, object=book, author=request.user)
        rating_form = RatingForm(data=request.POST, instance=rating)
        if rating_form.is_valid() and rating.author == request.user:
            rating = rating_form.save(commit=False)
            rating.object = book
            rating.save()
            messages.add_message(request, messages.SUCCESS, f'Your rating for {book.title} has been saved!')
        else:
            messages.add_message(request, messages.ERROR, 'There was an error updating your rating')

    return HttpResponseRedirect(reverse('book_detail', args=[slug]))


def delete_review(request, slug):
    """
    Docstring for delete_review
    
    :param request: Description
    :param slug: Description
    """
    book = get_object_or_404(Book, slug=slug)
    review = get_object_or_404(Review, object=book, author=request.user)
    if review.author == request.user:
        review.delete()
        messages.add_message(request, messages.SUCCESS, 'Your review has been deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own review!')


def delete_rating(request, slug):
    """
    Docstring for delete_rating
    
    :param request: Description
    :param slug: Description
    """
    book = get_object_or_404(Book, slug=slug)
    rating = get_object_or_404(Rating, object=book, author=request.user)
    if rating.author == request.user:
        rating.delete()
        messages.add_message(request, messages.SUCCESS, 'Your rating has been deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own rating!')
