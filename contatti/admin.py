
from django.contrib import admin
from .models import  *

class ContattiInline(admin.StackedInline):
    model = Contatti
    fields = ['data','agente','note','proposta','evidenziato','da_chiamare']
    #inlines = [StudentiInline]
    extra = 0

@admin.register(Aziende)
class AziendeAdmin(admin.ModelAdmin):
     list_display = ['nome','categoria','citta']
     list_filter = ['citta','provincia']
     inlines = [ContattiInline]

@admin.register(Agenti)
class AgentiAdmin(admin.ModelAdmin):
     list_display = ['nome','cognome','email']

@admin.register(RichiesteContatti)
class RichiesteContattiAdmin(admin.ModelAdmin):
     list_display = ['id','data','nome','cognome','email','telefono','interessi','note']

@admin.register(Condizioni)
class CondizioniAdmin(admin.ModelAdmin):
     list_display = ['user','tipologia','descrizione','prezzo']
     list_filter = ['tipologia']



