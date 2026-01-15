from django.urls import path
from . import views

urlpatterns = [
    path("", views.profile_page, name="profile_page"),
    path("read/", views.books_read, name="profile_read"),
    path("wishlist/", views.books_wishlist, name="profile_wishlist"),
    path("add-to-wishlist/<slug:slug>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("add-to-currently-reading/<slug:slug>/", views.add_to_currently_reading, name="add_to_currently_reading"),
    path("add-to-read/<slug:slug>/", views.add_to_read, name="add_to_read"),
    path("add-to-dnf/<slug:slug>/", views.add_to_dnf, name="add_to_dnf"),
    path("delete-status/<slug:slug>/", views.delete_status, name="delete_status"),
]
