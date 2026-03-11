from django import forms
from .models import Profilo

class ProfiloForm(forms.ModelForm):

    class Meta:
        model = Profilo
        fields = ['immagine_profilo']