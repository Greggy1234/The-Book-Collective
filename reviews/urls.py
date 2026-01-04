from django.urls import path
from . import views

urlpatterns = [
    path("", views.recent_reviews, name="homepage"),
    path("reviews/", views.all_reviews, name="all-reviews"),
    path("reviews/<slug:slug>/", views.review_detail, name="review_detail")
]
