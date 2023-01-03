from django.shortcuts import render
from contatti.models import *
from .filters import AziendeFilter
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import *
from django.http import HttpResponseRedirect

def index(request):
    
    context = {}
    return render(request,'contatti/index.html',context)

@login_required
def aziende(request):
    # fornisce l'elenco della aziende presenti nel database
    elenco = Aziende.objects.all()
   
    numero_aziende = len(elenco)
    myfilter = AziendeFilter(request.GET,queryset=elenco)
    elenco = myfilter.qs

    pag = Paginator(elenco,12)
    totpagine = pag.num_pages
    numpag = request.GET.get('pagina',1)
    pagelist = range(int(numpag)+1,totpagine+1)
    pagelist0 = range(1,int(numpag))
    pagina = pag.page(numpag)

    #context = {'elenco':elenco,'myfilter':myfilter,}
    context = {'object_list': pagina,           # la pagina con i dati da visualizzare
               'myfilter':myfilter,
               'totpagine': totpagine,
               'numpag' : numpag,
               'pagelist': pagelist, 
               'pagelist0': pagelist0,
               'numero_aziende' : numero_aziende
              }
    # context['user'] = visualizza_utente(request)
    return render(request,"contatti/aziende.html",context)

def dettaglio_azienda(request,id):
    # mostra i dati dell'aziende e dei contatti associati
    azienda = Aziende.objects.get(id=id)
    contatti = azienda.contatti_set.all()
    agenti = Agenti.objects.all()

    # se la funzione è richiamata con i parametri significa che voglio salvare il nuovo contatto
    
    contatto = request.GET.get('contatto','')
    note = request.GET.get('note','')
    agente = request.GET.get('agente','')
    if contatto:
        obj = Contatti.objects.get(id=contatto)
        obj.note = note
        nuovo_agente = Agenti.objects.get(id=agente)
        obj.agente = nuovo_agente
        obj.save()

    context = {'azienda':azienda, 'contatti': contatti, 'agenti':agenti,}
    #context['user'] = visualizza_utente(request)
    form = ContactForm(initial={'azienda':azienda.id,})
    context['form'] = form
    return render(request,"contatti/dettaglio_azienda.html",context) 

def contatti(request):
    # elenco dei contatti in ordine decrescente di data
    contatti = Contatti.objects.all()
    context = {'contatti': contatti}
    return render(request,"contatti/contatti.html",context) 

def add_contatto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            idazienda = form.cleaned_data['azienda']
            agente= form.cleaned_data['agente']
            note = form.cleaned_data['note']
            contatto = Contatti()
            azienda = Aziende.objects.get(id=idazienda)
            contatto.azienda = azienda
            contatto.agente = agente
            contatto.note = note
            contatto.save()
    return HttpResponseRedirect('aziende/'+str(idazienda))

def cancella_contatto (request):
    # cancella un contatto - non ancora testato
    # idcontatto = request.GET.get('idcontatto')
    idcontatto = request.GET.get('idcontatto')
    idazienda = request.GET.get('idazienda')
    record = Contatti.objects.get(id=idcontatto)
    record.delete()
   
    return HttpResponseRedirect('aziende/'+ str(idazienda))
