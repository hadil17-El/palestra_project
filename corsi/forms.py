from django import forms
from .models import Profile

class ProfiloForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['immagine_profilo']