from django.db import models
from django.contrib.auth.models import User
from book.models import Book


# Create your models here.
RATING_OPTIONS = ((0, 1), (1, 1.25), (2, 1.5), (3, 1.75),
                  (4, 2), (5, 2.25), (6, 2.5), (7, 2.75),
                  (8, 3), (9, 3.25), (10, 3.5), (11, 3.75),
                  (12, 4), (13, 4.25), (14, 4.5), (15, 4.75), (16, 5))


class Review(models.Model):
    """
    Stores a single instance of a review entry,
    related to :model:`book.Book` and :model:`auth.User`
    """
    object = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_review"
        )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review_author"
    )
    review = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f'Review of {self.object} by {self.author}'


class Rating(models.Model):
    """
    Stores the numerical rating of a book by a user,
    related to :model:`book.Book` and :model:`auth.User`
    """
    object = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_rating"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rating_author"
    )
    rating = models.IntegerField(choices=RATING_OPTIONS, default=16)
