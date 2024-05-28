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
        fields = ['archivio','nome','citta','provincia']

class ContattiFilter(django_filters.FilterSet):
  
    azienda = CharFilter(field_name="azienda__nome",lookup_expr="icontains")
    citta = CharFilter(field_name="azienda__citta",lookup_expr="icontains")
    provincia = CharFilter(field_name = "azienda__provincia",lookup_expr="icontains")
    note = CharFilter(field_name="note",lookup_expr="icontains")
    da_chiamare = ChoiceFilter(field_name="da_chiamare", choices=DA_CHIAMARE, method='filtro_attivo')

    class Meta: 
        model=Contatti
        fields=['azienda','citta','note','da_chiamare']

    def __init__(self, *args, **kwargs):
        super(ContattiFilter, self).__init__(*args, **kwargs)
        self.filters['provincia'].field.widget.attrs.update({'class': 'custom-province-field'})

    def filtro_attivo(self, queryset, name, value):
        if value == '1':
            return queryset.filter(da_chiamare=True)
        return queryset

    
  

 
    