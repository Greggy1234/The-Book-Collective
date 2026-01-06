from django.urls import path
from . import views

urlpatterns = [
    path("", views.BookOverview.as_view(), name="book_overview"),
    path("search/", views.BookSearch.as_view(), name="book_search"),
    path("add-book/", views.add_book, name="add_book"),
    path("<slug:slug>/", views.book_detail, name="book_detail"),
    path("<slug:slug>/add-review", views.add_review, name="add_review"),
    path("<slug:slug>/add-rating", views.add_rating, name="add_rating"),
    path("<slug:slug>/edit-review", views.edit_review, name="edit_review"),
    path("<slug:slug>/edit-rating", views.edit_rating, name="edit_rating"),
    path("<slug:slug>/delete-review", views.delete_review, name="delete_review"),
    path("<slug:slug>/delete-rating", views.delete_rating, name="delete_rating"),
]
