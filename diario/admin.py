from django.contrib import admin
from .models import Diario, Alimento, Consumazione, ProfiloUtente
from datetime import date

WEEKDAYS = ('lunedi','martedi','mercoledi','giovedi','venerdi','sabato','domenica')

class ConsumazioneInline(admin.TabularInline):
    model = Consumazione
    extra = 1

@admin.register(Diario)     
class DiarioAdmin(admin.ModelAdmin):
    fields = ['user','data','note']
    list_display = ['user','data_registrazione','note']
    inlines =[ConsumazioneInline]
    
    def data_registrazione(self,obj):
        return WEEKDAYS[obj.data.isocalendar()[2]-1] + " " + obj.data.strftime("%d/%m/%Y")
             
#admin.site.register(Diario,DiarioAdmin)
#admin.site.register(Alimento)
@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    fields = ['user','nome','calorie','categoria']
    list_display = ['user','nome']

admin.site.register(ProfiloUtente)


