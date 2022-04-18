from django.shortcuts import render
from OffPcto.models import *
from django.templatetags.static import static

from .filters import AziendeFilter

def index(request):
    return render(request,'index.html',{})
    
def tutor(request):
     elenco = Tutor.objects.all()
     context = {'object_list':elenco}
     return render(request,"tutor.html",context)

def aziende(request):
    elenco = Aziende.objects.all()

    myfilter = AziendeFilter(request.GET,queryset=elenco)
    elenco = myfilter.qs
    context = {'object_list': elenco, 'myfilter':myfilter}
    return render(request,"aziende.html",context)

def carica_tutor(request):
   
    url = 'http://mapelli.selfip.org/pcto/dati/tutor.csv'
    f = open(url,'r')
    listaRighe = f.readlines()    # legge tutte le righe del file e restituisce la lista delle righe
    f.close()                     # chiudo il file
    testa = listaRighe[0].strip() # memorizza in testa, la prima riga
    self.campi = testa.strip().split(',')   # inizializza self.campi con la lista dei campi
    listaRighe = listaRighe[1:]   # toglie la prima riga da listaRighe
    context = {'righe': listaRighe}
    return render(request,"caricaTutor",context)
    
