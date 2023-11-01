from django.contrib import admin
from .models import  Aziende, Agenti, Contatti, RichiesteContatti

class ContattiInline(admin.StackedInline):
    model = Contatti
    fields = ['data','agente','note']
    #inlines = [StudentiInline]
    extra = 0

@admin.register(Aziende)
class AziendeAdmin(admin.ModelAdmin):
     list_display = ['nome','categoria','citta']
     inlines = [ContattiInline]

@admin.register(Agenti)
class AgentiAdmin(admin.ModelAdmin):
     list_display = ['nome','cognome','email']

@admin.register(RichiesteContatti)
class RichiesteContattiAdmin(admin.ModelAdmin):
     list_display = ['id','data','nome','cognome','email','telefono','interessi','note']
       


