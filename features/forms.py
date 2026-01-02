from django import forms
from .models import FutureFeatures


class FeaturesForm(forms.ModelForm):
    class Meta:
        model = FutureFeatures
        fields = ("name", "message",)
