from django.db import models


# Create your models here.
class FutureFeature(models.Model):
    """
    Stores information for the upcoming changes to the app
    """
    STATUS_OPTION = ((1, "Currently Working On"),
                     (2, "Next in line"),
                     (3, "Pre-Planning Stage"),
                     (4, "Not on radar"),
                     )
    feature = models.TextField(unique=True)
    status = models.CharField(choices=STATUS_OPTION, default=4)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class FutureFeaturesForm(models.Model):
    """
    Stores information from the features form
    """
    name = models.CharField(max_length=200)
    message = models.TextField()
