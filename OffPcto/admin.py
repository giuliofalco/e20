from django.contrib import admin
from .models import Tutor, Aziende

#admin.site.register(Tutor)
#admin.site.register(Aziende)

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ['cognome','nome','email','classi']

@admin.register(Aziende)
class AziendeAdmin(admin.ModelAdmin):
    list_display = ['ragione_sociale','sede_comune','sede_provincia']
