from django.shortcuts import render
from contatti.models import *
from .filters import AziendeFilter
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def index(request):
    
    context = {}
    return render(request,'contatti/index.html',context)

@login_required
def aziende(request):
    # fornisce l'elenco della aziende presenti nel database
    elenco = Aziende.objects.all()
   
    # numero_aziende = len(elenco)
    myfilter = AziendeFilter(request.GET,queryset=elenco)
    elenco = myfilter.qs
    context = {'elenco':elenco,'myfilter':myfilter,}

   # pag = Paginator(elenco,20)
   # totpagine = pag.num_pages
   # numpag = request.GET.get('pagina',1)
   # pagelist = range(int(numpag)+1,totpagine+1)
   # pagelist0 = range(1,int(numpag))
   # pagina = pag.page(numpag)

   # context = {'object_list': pagina,           # la pagina con i dati da visualizzare
   #            'myfilter':myfilter,
   #            'totpagine': totpagine,
   #            'numpag' : numpag,
   #            'pagelist': pagelist, 
   #            'pagelist0': pagelist0,
   #            'numero_aziende' : numero_aziende
   #           }
   # context['user'] = visualizza_utente(request)
    return render(request,"contatti/aziende.html",context)
