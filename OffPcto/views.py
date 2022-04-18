from django.shortcuts import render
from OffPcto.models import *
from django.templatetags.static import static
from django.core.paginator import Paginator,EmptyPage

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

    pag = Paginator(elenco,20)
    totpagine = pag.num_pages
    pagelist = range(1,totpagine+1)
    numpag = request.GET.get('pagina',1)
    pagina = pag.page(numpag)

    context = {'object_list': pagina,           # la pagina con i dati da visualizzare
               'myfilter':myfilter,
               'totpagine': totpagine,
               'numpag' : numpag,
               'pagelist': pagelist, 
              }
    return render(request,"aziende.html",context)

    
