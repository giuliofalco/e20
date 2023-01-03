import django_filters
from django_filters import CharFilter, ChoiceFilter
from .models import *


class AziendeFilter(django_filters.FilterSet):
    archivio = ChoiceFilter(field_name="archivio",choices=ARCHIVIO)
    nome = CharFilter(field_name="nome",lookup_expr="icontains")
    citta = CharFilter(field_name="citta",lookup_expr="icontains")
    provincia = CharFilter(field_name="provincia",lookup_expr="icontains")
    
    class Meta:
        model = Aziende
        fields = []


 
    