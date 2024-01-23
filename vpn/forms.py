from django import forms
from vpn.models import Site


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["url", "name"]
