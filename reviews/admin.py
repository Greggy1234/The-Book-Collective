from django.contrib import admin
from .models import Review, Rating, Like

# Register your models here.
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Like)
