from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from book.models import Book


# Create your models here.
class Status(models.Model):
    """
    Stores an instance of the status of a book in relation to a user,
    related to :model:`book.Book` and :model:`auth.User`
    """
    STATUS_OPTION = ((1, "On Wishlist"),
                     (2, "Currently Reading"),
                     (3, "Read"),
                     (4, "Did Not Finished"))
    object = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_status"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_book_status"
    )
    status = models.CharField(choices=STATUS_OPTION, default=1)
    started_on = models.DateTimeField(blank=True, null=True)
    finished_on = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["object", "author"], name="unique_status")
        ]

    def save(self, *args, **kwargs):
        if self.status == 2 and not self.started_on:
            self.started_on = timezone.now()

        if self.status == 3 and not self.finished_on and not self.started_on:
            self.started_on = timezone.now()
            self.finished_on = timezone.now()
        elif self.status == 3 and not self.finished_on:
            self.finished_on = timezone.now()

        super().save(*args, **kwargs)
