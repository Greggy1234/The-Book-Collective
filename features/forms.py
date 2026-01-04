from django import forms
from .models import FutureFeaturesForm


class FeaturesForm(forms.ModelForm):
    class Meta:
        model = FutureFeaturesForm
        fields = ("name", "message",)
