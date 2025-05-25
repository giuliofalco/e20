from django.shortcuts import render
from django.shortcuts import get_object_or_404
from contatti.models import *
from .filters import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import modelform_factory 
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
from django.conf import settings
# Definisci gli SCOPES necessari per interagire con Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

@login_required
def index(request):
    
    context = {}
    return render(request,'contatti/index.html',context)

@login_required
def aziende(request):
    # fornisce l'elenco della aziende presenti nel database
    elenco = Aziende.objects.filter(user=request.user)
   
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

@login_required
def dettaglio_azienda(request,id):
    # mostra i dati dell'aziende e dei contatti associati
    azienda = Aziende.objects.get(id=id)
    contatti = azienda.contatti_set.all()
    agenti = Agenti.objects.all()

    # se la funzione è richiamata con i parametri significa che voglio salvare il nuovo contatto
    
    contatto = request.GET.get('contatto','')
    note = request.GET.get('note','')
    agente = request.GET.get('agente','')
    evidenziato = request.GET.get('evidenziato','')
    da_chiamare = request.GET.get('da_chiamare','')
    if contatto:
        obj = Contatti.objects.get(id=contatto)
        obj.note = note
        nuovo_agente = Agenti.objects.get(id=agente)
        obj.agente = nuovo_agente
        obj.evidenziato = evidenziato != ''
        obj.da_chiamare = da_chiamare != ''
        obj.save()

    context = {'azienda':azienda, 'contatti': contatti, 'agenti':agenti,}
    #context['user'] = visualizza_utente(request)
    form = ContactForm(initial={'azienda':azienda.id,})
    context['form'] = form
    return render(request,"contatti/dettaglio_azienda.html",context) 

@login_required
def contatti(request):
    # elenco dei contatti in ordine decrescente di data
    contatti = Contatti.objects.filter(user=request.user)
    
    myFilter = ContattiFilter(request.GET,queryset=contatti)
    contatti = myFilter.qs
    context = {'contatti': contatti,'myFilter': myFilter}
    
    
    return render(request,"contatti/contatti.html",context) 

@login_required
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
            contatto.user = request.user
            contatto.save()
    return HttpResponseRedirect('aziende/'+str(idazienda))

@login_required
def cancella_contatto (request):
    # cancella un contatto - non ancora testato
    # idcontatto = request.GET.get('idcontatto')
    idcontatto = request.GET.get('idcontatto')
    idazienda = request.GET.get('idazienda')
    record = Contatti.objects.get(id=idcontatto)
    record.delete()
   
    return HttpResponseRedirect('aziende/'+ str(idazienda))

def insertCompany(request):
    # inserisce una nuova azienda
    
    form = AziendeForm()
    if request.method == 'POST':
        form = AziendeForm(request.POST)
        if form.is_valid():
           form.save(commit=False)
           form.instance.user = request.user
           form.save()
           return HttpResponseRedirect("/contatti/aziende")    
    template = "insertCompany.html"
    context = {'form': form, 'modifica': False}
    return(render(request,template,context))


def updateCompany(request, id):
    azienda = get_object_or_404(Aziende, pk=id, user=request.user)
    if request.method == 'POST':
        form = AziendeForm(request.POST, instance=azienda)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/contatti/aziende")
    else:
        form = AziendeForm(instance=azienda)

    template = "insertCompany.html"  # stesso template
    context = {'form': form, 'modifica': True, 'azienda_id': id }
    return render(request, template, context)


def richieste_contatti(request):
    # permette di visualizzare e ricevere i dati di una form di contatti dei potenziali clienti
    if request.method == "POST":
        myform=ContattiForm(request.POST)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': '6LerqUspAAAAAAMQSSxFve-GNSfN52gUgQj0_Mh9 ',
            'response': recaptcha_response }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        if myform.is_valid() and response.json()['success'] : 

            cognome = request.POST.get('cognome')
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            telefono = request.POST.get('telefono')
            interessi = request.POST.get('interessi')
            note = request.POST.get('note')
            contatto = RichiesteContatti()
            contatto.cognome = cognome
            contatto.nome = nome
            contatto.email = email
            contatto.telefono = telefono
            contatto.interessi = interessi
            contatto.note = note
            contatto.save()  # Salva la richiesta di contattto nel database
            context={}
            return render(request,"contatti/conferma.html",context)
    else:
        myform=ContattiForm()
        
    context = {"myform":myform}
    return render(request,"contatti/richieste_contatti.html",context)

def calendario(request,start,end,target,msg):
    # inserisce l'evento in calendario. Su account info@e20.website

    # Percorso per il file token.pickle che memorizza il token di accesso
    token_path = os.path.join(settings.CREDENTIALS_PATH, 'token.pickle')
    # Percorso per il file credentials.json che hai scaricato da Google Cloud Console
    credentials_path = os.path.join(settings.CREDENTIALS_PATH, 'credentials.json')

    creds = None

    # Controlla se esiste già un token di accesso salvato
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token_file:
            creds = pickle.load(token_file)
    
    # Se non ci sono credenziali valide, esegui il flusso di autenticazione
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva il token di accesso per le esecuzioni future
        with open(token_path, 'wb') as token_file:
            pickle.dump(creds, token_file)

    # Costruisci il servizio Google Calendar
    service = build('calendar', 'v3', credentials=creds)

    # Definisci l'evento di prova da aggiungere al calendario
    event = {
        'summary': 'Evento da Contatti',
        'location': 'Monza, Italia',
        'description': f'{msg} {target}',
        'start': {
            'dateTime': f'{start}',
            'timeZone': 'Europe/Rome',
        },
        'end': {
            'dateTime': f'{end}',
            'timeZone': 'Europe/Rome',
        },
        'attendees': [
            {'email': 'gfalco58@gmail.com'},         # sostituire con indirizzo email del destinatario
            {'email': 'barbara.bbiagini@gmail.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    # Inserisci l'evento nel calendario
    event = service.events().insert(calendarId='primary', body=event).execute()
    return HttpResponse(f'Evento registrato con successo');
