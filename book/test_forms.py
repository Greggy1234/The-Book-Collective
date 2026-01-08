from django.test import TestCase
from .forms import AddBook, AddAuthor
from .models import Genre, Author, Language


class TestAuthorForm(TestCase):
    def test_form_is_valid(self):
        """ Test for all fields """
        form = AddAuthor({
            'author': 'Jane Austen'
        })
        self.assertTrue(form.is_valid(), msg="Form is not valid")

    def test_form_is_not_valid_author(self):
        """ Test for no author field """
        form = AddAuthor({
            'author': ''
        })
        self.assertFalse(form.is_valid(), msg="No author field given in test")


class TestBookForm(TestCase):
    def setUp(self):
        self.author = Author.objects.create(author="Jane Austen")
        self.language = Language.objects.create(lang="English")
        self.genre = Genre.objects.create(genre="Romance")

    def test_form_is_valid(self):
        """
        Test for all fields
        For test to work, you have to comment out the def __init__
        method in :form:`book.AddBook' as that stops validity of id=1
        """
        form = AddBook({
            'author': [self.author.id],
            'genres': [self.genre.id],
            'language': self.language.id,
            'title': 'Pride and Prejudice',
            'pages': '300',
            'synopsis': 'Boy and girl meet',
            'published': '1813'
        })
        print(form.errors)
        self.assertTrue(form.is_valid(), msg="Form is not valid")
