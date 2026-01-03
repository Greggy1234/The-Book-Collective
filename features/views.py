from django.shortcuts import render
from django.contrib import messages
from .models import FutureFeatures
from .forms import FeaturesForm


# Create your views here.
def features_page(request):
    """
    Returns all objects in the :model:`FutureFeatures`
    as long as they are not classed as 'not on radar'
    Shows the future features sugestion form
    
    **Context**
    
    **Template**
    """
    features = FutureFeatures.objects.exclude(status=4).order_by('-updated_on')

    if request.method == "POST":
        feature_form = FeaturesForm(data=request.POST)
        if feature_form.is_valid():
            feature_form.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Thank you for your suggestion. We will review all suggestions sent through!'
            )

    feature_form = FeaturesForm()

    return render(
        request,
        "features/features.html",
        {
            "features": features,
            "feature_form": feature_form,
        }
    )
