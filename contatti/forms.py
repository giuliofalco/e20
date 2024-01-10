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
         fields = ['archivio','nome','indirizzo','citta','phone','mail']

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

