from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django_extensions.db.fields import AutoSlugField
from cloudinary.models import CloudinaryField
import datetime


# Taken from https://stackoverflow.com/questions/49051017/year-field-in-django
def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


# Create your models here.
class Genre(models.Model):
    """
    Stores the list of genres available for the Book model
    """
    genre = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return f'{self.genre}'


class Author(models.Model):
    """
    Stores the list of authors available for the Book model
    """
    author = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f'{self.author}'


class Language(models.Model):
    """
    Stores the list of languages available for the Book model
    """
    lang = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.lang}'


class Book(models.Model):
    """
    Stores a single book entry related to :model:`book.Genre`,
    :model:`book.Author` and :model:`book.Language`
    """
    title = models.CharField(max_length=250)
    # Taken from https://stackoverflow.com/questions/49051017/year-field-in-django
    published = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1000), max_value_current_year])
    pages = models.PositiveIntegerField(verbose_name="Number of Pages",
                                        validators=[MinValueValidator(1)])
    author = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)
    language = models.ForeignKey(Language, default=1,
                                 on_delete=models.SET_DEFAULT)
    synopsis = models.TextField(blank=True)
    front_cover = CloudinaryField('image', default='placeholder')
    created_on = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='title')

    class Meta:
        ordering = ["title"]

    def avg_rating(self):
        average = self.book_rating.aggregate(Avg('rating'))['rating__avg']
        if not average:
            return None
        average_round = round(average, 2)
        return average_round

    def __str__(self):
        return f'{self.title} by {self.author}, released in {self.first_published}'
