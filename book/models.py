from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Genre(models.Model):
    genre = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return f'This genre is {self.genre}'


class Author(models.Model):
    author = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f'This author is {self.author}'


class Language(models.Model):
    lang = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'This language is {self.lang}'


class Book(models.Model):
    title = models.CharField(max_length=250)
    first_published = models.DateField()
    pages = models.PositiveIntegerField(verbose_name="Number of Pages",
                                        validators=[MinValueValidator(1)])
    author = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)
#    #avg_rating
    language = models.ForeignKey(Language, default="Language to be added",
                                 on_delete=models.SET_DEFAULT)
    synopsis = models.TextField(blank=True)
#    #front_cover
    created_on = models.DateTimeField(auto_now_add=True)
