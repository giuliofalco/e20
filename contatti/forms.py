from datetime import date
from django import forms
from contatti.models import *

class DateInput(forms.DateInput):
    input_type='date'

class ContactForm(forms.Form):
    azienda = forms.CharField(label='ID Azienda',max_length=10)
    agente  = forms.ModelChoiceField(label='Agente', queryset=Agenti.objects.all(), empty_label=None)
    note = forms.CharField(widget=forms.Textarea,required=False)

