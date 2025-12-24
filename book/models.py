from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Genre(models.Model):
    """
    Stores the list of genres available for the Book class
    """
    genre = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return f'This genre is {self.genre}'


class Author(models.Model):
    """
    Stores the list of authors available for the Book class
    """
    author = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f'This author is {self.author}'


class Language(models.Model):
    """
    Stores the list of languages available for the Book class
    """
    lang = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'This language is {self.lang}'


class Book(models.Model):
    """
    Stores a single book entry related to :model:`book.Genre`,
    :model:`book.Author` and :model:`book.Language`
    """
    title = models.CharField(max_length=250)
    first_published = models.DateField()
    pages = models.PositiveIntegerField(verbose_name="Number of Pages",
                                        validators=[MinValueValidator(1)])
    author = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)
#    #avg_rating
    language = models.ForeignKey(Language, default=1,
                                 on_delete=models.SET_DEFAULT)
    synopsis = models.TextField(blank=True)
#    #front_cover
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f'{self.title} by {self.author}, released in {self.first_published}'
