from datetime import date
from django import forms
from contatti.models import *
from django.forms import ModelForm
from django_recaptcha.fields import ReCaptchaField

class DateInput(forms.DateInput):
    input_type='date'

class ContactForm(forms.Form):
    azienda = forms.CharField(label='ID Azienda',max_length=10)
    agente  = forms.ModelChoiceField(label='Agente', queryset=Agenti.objects.all(), empty_label=None)
    note = forms.CharField(widget=forms.Textarea,required=False)

class AziendeForm(ModelForm):
    class Meta:
         model = Aziende
         fields = ['archivio','nome','indirizzo','citta','provincia','phone','mail','web']

class ContattiForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = RichiesteContatti
        fields = ['nome','cognome','email','telefono','interessi','note']
        labels = {
            'nome': 'Nome',
            'cognome':'Cognome',
            'email' : 'Email',
            'telefono' : 'Telefono',
            'interessi' : 'Interessi',
            'note' : 'Note',
        }
# contatti/forms.py

class CondizioniForm(forms.ModelForm):
    class Meta:
        model = Condizioni
        fields = ["tipologia", "descrizione", "prezzo"]
        widgets = {
            "tipologia": forms.TextInput(attrs={"class": "form-control"}),
            "descrizione": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "prezzo": forms.NumberInput(attrs={"class": "form-control"}),
        }

