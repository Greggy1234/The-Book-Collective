from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile_page, name="profile-page"),
    path("read/", views.books_read, name="profile_wishlist"),
    path("wishlist/", views.books_wishlist, name="profile_wishlist"),
]
