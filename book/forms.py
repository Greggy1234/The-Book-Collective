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

    def __init__(self, *args, **kwargs):
        super(AddBook, self).__init__(*args, **kwargs)
        self.fields["author"].queryset = Author.objects.exclude(id=1)
        self.fields["genres"].queryset = Genre.objects.exclude(id=1)
        self.fields["language"].queryset = Language.objects.exclude(id=1)
