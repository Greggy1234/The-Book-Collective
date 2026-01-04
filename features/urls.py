from django.urls import path
from . import views

urlpatterns = [
    path("", views.features_page, name="features")
]
