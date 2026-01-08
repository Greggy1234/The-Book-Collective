from django import forms
from .models import Author, Book, Language, Genre


class AddAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("author",)


class AddBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("author", "title", "pages", "synopsis", "published", "genres", "language")

    def __init__(self, **kwargs):
        super(AddBook, self).__init__(self, **kwargs)
        self.fileds["author"].queryset = Author.objects.exclude(id=1)
        self.fileds["genres"].queryset = Genre.objects.exclude(id=1)
        self.fileds["language"].queryset = Language.objects.exclude(id=1)
