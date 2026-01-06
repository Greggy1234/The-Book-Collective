from django import forms
from .models import Author, Book


class AddAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("author",)


class AddBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "pages", "synopsis", "published", "author", "genres", "language")
