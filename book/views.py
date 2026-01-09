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
    Returns all objects in :model:`book.Book`, paginated so
    only 12 books max appear per page

    **Context**
    ``books``
        All published instances of :model:`book.Book`
    ``paginate_by``
        Number of posts per page.

    **Template**
    :template:`book/books.html`
    """
    model = Book
    template_name = "book/books.html"
    context_object_name = "books"
    paginate_by = 12


class BookSearch(ListView):
    """
    Returns a list of all objects from :model:`book.Book`
    where the query matches the either the author or book title
    paginated so only 12 books max appear per page

    **Context**
    ``book_search``
        All published instances of :model:`book.Book` that match
        the query
    ``paginate_by``
        Number of posts per page.

    **Template**
    :template:`book/book_search.html`
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
    Displays an individual :model:`book.Book`

    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``review``
        All instances of :model:`reviews.Review` related to book
    ``rating``
        All instances of :model:`reviews.Rating` related to book
    ``review_count``
        A count of all the reviews on the book
    ``user_review``
        The logged in user's specific review if available.
        Using first as it there can only be one per book per user
        thus reducing needing to iterate over the queryset in the template
    ``user_rating``
        The logged in user's specific rating if available.
        Using first for the same reason as above
    ``user_status``
        The logged in user's specific book status if available.
        Using first for the same reason as above.
        Taken from :model:`status.Status`

     **Template**
        :template:`book/book-detail.html`
    """
    book = get_object_or_404(Book, slug=slug)
    review = book.book_review.all().order_by("-created_on")
    rating = book.book_rating.all().order_by("-created_on")
    review_count = book.book_review.count()
    user_review = book.book_review.filter(object=book, author=request.user).first()
    user_rating = book.book_rating.filter(object=book, author=request.user).first()
    user_status = book.book_status.filter(object=book, author=request.user).first()

    return render(
        request,
        "book/book-detail.html",
        {
            "book": book,
            "rating": rating,
            "review": review,
            "review_count": review_count,
            "user_review": user_review,
            "user_rating": user_rating,
            "user_status": user_status,
        }
    )


def add_book(request):
    """
    Returns the add book form

    **Context**
    ``add_book_form``
        An instance of :form:`book.AddBook`

     **Template**
        :template:`book/add-book.html`
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
    Returns the add author form, to be used only on
    the add book page
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
    Adds a users review to :model:`reviews.Review`

    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``review_form``
        An instance of :form:`reviews.ReviewForm`
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
    Adds a users rating to :model:`reviews.Rating`
    
    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``rating_form``
        An instance of :form:`reviews.RatingForm`
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
    Edit a users review

    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``review``
        A single review related to the book
    ``review_form``
        An instance of :form:`reviews.ReviewForm`
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
    Edit a users rating

    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``rating``
        A single rating related to the book
    ``rating_form``
        An instance of :form:`reviews.RatingForm`
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
    Delete an idividual review

    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``review``
        A single review related to the book
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
    Delete an idividual rating

    **Context**
    ``book``
        An instance of :model:`book.Book`
    ``rating``
        A single rating related to the book
    """
    book = get_object_or_404(Book, slug=slug)
    rating = get_object_or_404(Rating, object=book, author=request.user)
    if rating.author == request.user:
        rating.delete()
        messages.add_message(request, messages.SUCCESS, 'Your rating has been deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own rating!')
