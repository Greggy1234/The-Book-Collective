from django.urls import path
from . import views

urlpatterns = [
    path("", views.recent_reviews, name="homepage"),
    path("reviews/", views.all_reviews, name="all_reviews"),
    path("reviews/<slug:slug>/", views.review_detail, name="review_detail"),
    path("reviews/<slug:slug>/add-review-like", views.add_review_like, name="add_review_like"),
    path("reviews/<slug:slug>/delete-review-like", views.delete_review_like, name="delete-review_like"),
]
