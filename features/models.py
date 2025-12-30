from django.db import models


# Create your models here.
class FutureFeatures(models.Model):
    """
    Stores information from the features form
    """
    name = models.CharField(max_length=200)
    message = models.TextField()
