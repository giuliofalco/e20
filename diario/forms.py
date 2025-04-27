from django import forms
from .models import ProfiloUtente

class ProfiloUtenteForm(forms.ModelForm):
    class Meta:
        model = ProfiloUtente
        fields = ['immagine_sfondo']