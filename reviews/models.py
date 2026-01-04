from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from book.models import Book


# Create your models here.
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


    def number_likes(self):
        return self.review_like.count()


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
    rating = models.DecimalField(max_digits=3, decimal_places=2,
                                 validators=[
                                     MinValueValidator(1.00),
                                     MaxValueValidator(5.00)
                                 ])
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f'Rating of {self.object}: {self.rating}'


class Like(models.Model):
    """
    Stores an instance of a user liking a review,
    related to :model:`book.Book` and :model:`auth.User`
    """
    object = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="review_like"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="like_author"
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["object", "author"], name="unique_like")
        ]
