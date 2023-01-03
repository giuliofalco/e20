from django.contrib import admin
from .models import  Aziende

@admin.register(Aziende)
class AziendeAdmin(admin.ModelAdmin):
     list_display = ['nome','categoria','citta']