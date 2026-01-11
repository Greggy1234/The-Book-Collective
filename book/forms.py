from django import forms
from .models import Author, Book, Language, Genre


class AddAuthor(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("author",)


class AddBook(forms.ModelForm):
    pages = forms.IntegerField(widget=forms.TextInput)
    published = forms.IntegerField(widget=forms.TextInput)
    author = forms.ModelMultipleChoiceField(queryset=Author.objects, widget=forms.CheckboxSelectMultiple)
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Book
        fields = ("author", "title", "pages", "synopsis", "published", "genres", "language")

    def __init__(self, *args, **kwargs):
        super(AddBook, self).__init__(*args, **kwargs)
        self.fields["author"].queryset = Author.objects.exclude(id=1).order_by("author")
        self.fields["genres"].queryset = Genre.objects.exclude(id=1).order_by("genre")
        self.fields["language"].queryset = Language.objects.exclude(id=1).order_by("lang")
        self.fields["language"].initial = Language.objects.get(lang="English")
