from django.urls import path
from . import views

urlpatterns = [
    path("", views.book_overview.as_view(), name="book_overview"),
    path("<slug:slug>/", views.book_detail, name="book_detail")
]
