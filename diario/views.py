#from typing_extensions import Required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from diario.models import Diario, Consumazione, Alimento
from django.template import loader
from django.urls import reverse
from . import myDate 
#from datetime import date
import datetime as dt
from django.contrib.auth import authenticate, login

@login_required
def index(request):
   lista = Diario.objects.all()
   # costruisco la lista con i numeri delle settimane

   weeks = [giorno.week() for giorno in lista]    # lista con i dati compresi i duplicati
   weeks = set(weeks)                             # elimino i duplicati
   weeks = list(weeks)                            # trasformo in lista e 
   weeks.sort()                                   # metto in ordine crescente 

   # produco la lista organizzata per settimane
   # ogni elmento è il numero della settimana seguita dalla lista con gli oggetti Diario
   # appartenenti a quella settimana. 

   dati = [[sett,[oggetto for oggetto in lista if oggetto.week() == sett]] for sett in weeks]
   # genero una lista di liste. Ogni componente è una lista il cui primo elemento è 
   # il numero della settimana e il secondo è la lista che contiene le registrazioni 
   # di quella settimana 
   # es. [[7,[ogg1, ogg2, ogg3]], [11, [ogg4,ogg5]] ogni ogg è un oggetto di Diario
   
   context = {'lista_settimanale': dati}
 
   return render(request, 'diario/index.html', context)

@login_required
def settimana(request,w):
      from . import config
      
      lista = Diario.objects.all()                        # tutte le registrazioni
      weekly = [obj for obj in lista if obj.week() == w]  # solo quelle della settimana w   
      cons = [[w.week_day,list(w.consumazione_set.all())] for w in weekly]
      # estraggo da weekly (lista degli oggetti Diario di quella particolare settimana)
      # per ogni elemento di weekly le consumazioni ad esso associate. 
      # Trasformo il querySet in lista
      # produco una lista il cui elemnti sono il giorno della settimana 
      # ('lun', 'mart', seguito dalla data) e dalla lista delle consumazioni di quel giorno
     
      # per ottenere un report tabellare in cui ogni riga sia una consumazione e le colonne i
      # giorni:
      # preparo un dizionario in cui la chiave, sia il nome di una consumazione
      # e il valore una lista di elementi il cui primo elemento è il weekday, e il secondo
      # la lista degli alimenti della consumazione in quel giorno
      
      PASTI = ['fuori_pasto','colazione','merenda_mat','pranzo','merenda_pom','cena','dopo_cena']
      # inizializzo la struttura: lista con tante righe quanti sono i tipi di pasto
      # ogni righe è una lista, il primo elemento il nome del pasto, il secondo una lista di 7
      # elementi, ciascuno dei quali conterrà gli alimenti consumati in quel giorno e il quel pasto
      struttura = [[config.PASTIL[j], [["",0] for i in range(7)]] for j in range(len(config.PASTIL))]
      
      # riempio la struttura
      for obj in weekly:
          col = obj.w_day() - 1                    # la colonna è data dal giorno della settimana
          for cons in obj.consumazione_set.all():  # esplodo l'oggetto diario nelle sue
                                                   # consumazioni
              riga = cons.tipo_pasto               # il numero di riga corrisponde al tipo di pasto
              cont = cons.alimento.all()           # esplodo negli alimenti associati a 
                                                   # quella consumazione
              struttura[riga][1][col][0] = cont    # colloco gli alimenti nella corretta posizione
              struttura[riga][1][col][1] = obj.id  # ossia nel posto 0 nella lista piu interna
                                                   # e l'id nella posizione 1 della lista 
                                                   # più interna
      # mi serve per intestare le colonne della tabella
      GIORNI = ["lun","mar","mer","gio","ven","sab","dom"] 
     
      
      md = myDate.MyDate()                         
      periodo = md.str_week(w)                     # calcolo data di inizio e fine 
                                                   # della settimana w
      
      FRUTTA =  ['pompelmi','fragole']
      context = {'settimana': w,'struttura': struttura, 'pasti':config.PASTIL, 'periodo': periodo, 
                 'altro': FRUTTA, 'giorni': GIORNI}
                  
      return render(request,'diario/settimana.html',context)

from django.contrib.auth.decorators import login_required

@login_required 
def modifica(request,id,week,pasto,day): 
     from . import config 
     # apre il template omonimo che permette di inserire o cancellare alimenti di un 
     # particolare giorno della settimana. Attivata al click su una casella di settimana 
     # il parametro pasto è la sua versione stringa
     # PASTI = {'fuori_pasto':0,'colazione':1,'merenda_mat':2,'pranzo':3,'merenda_pom':4,
     #         'cena':5,'dopo_cena':6} 
     data = ""
     if id != 0: 
 
         diario = Diario.objects.get(id=id)              # l'oggetto registrazione con l'id 
                                                         # del parametro
         liscons = diario.consumazione_set.all()         # tutte le consumazioni relative a quell'id
         plist = liscons.filter(tipo_pasto = config.PASTIC[pasto])  # lista con la cons corrisp al
                                                         # tipo_pasto
         alimlist = plist[0].alimento.all()              # lista degli alimenti
         alimId = [al.id for al in alimlist]             # tutti gli id della lista di 
                                                         # alimenti trovati
         alims  = list(Alimento.objects.all())           # tutti gli alimenti, come lista
                                                         # di oggetti 
                                                        
         alimenti = [elem for elem in alims if elem.id not in alimId]
                                                        # gli alimenti non ancora scelti
         strdata = diario.data.strftime("%d/%m/%Y")
      
     else:
 
        alimlist = ""                                   # si richiede di creare un nuovo 
                                                        # oggetto Diario
        d = myDate.MyDate()
        miadata = d.data_wday(week,day-1)               # calcolo la data con la mia funzione
        data  = "{}-{}-{}".format(d.anno_corrente(),miadata[1]+1,miadata[0])     # formato data come tupla anno,mese,giorno
        strdata = "{}/{}/{}".format(d.anno_corrente(),miadata[1]+1,miadata[0])   # formato data come stringa europea
        alimenti = list(Alimento.objects.all())                     # tutti gli alimenti
     
     alimenti.sort(key=lambda x: x.nome.lower())
     context = {'alimlist': alimlist, 'id': id, 'pasto': config.PASTIC[pasto], 'strpasto': pasto,
                'alimenti' : alimenti,'data': data, 'giorno':day, 'strdata': strdata,
                'week':week,
               }
     
     return render(request,'diario/modifica.html',context)

@login_required  
def registra(request):
# registra la modifica effettuata aggiungendo un alimento al pasto della settimana 

    objid    = request.POST['objid']                          # lettura parametri
    giorno   = request.POST['giorno']
    miadata  = request.POST['data']
    pasto    = request.POST['pasto']
    alimento = request.POST['alimento']
    strpasto = request.POST['strpasto']
    
    if objid == '0':                                        # non ho l'id, ma non so ancora se l'oggetto esiste
       miodiario = Diario.objects.filter(data=miadata) # lo cerco attraverso la data, se esiste mi restituisce un Query Set con un solo elemento
       if miodiario:                                        # miodiario esiste
          miodiario = miodiario[0]                          # mio diario deve essere un oggetto, non un Query Set. Prendo l'unico oggetto della lista        
       else:                                                # non esiste, lo creo
          d = dt.datetime.strptime(miadata, "%Y-%m-%d")
          d = d.date()
          miodiario = Diario.objects.create(data=d) 
       consumazione = Consumazione.objects.create(diario=miodiario,tipo_pasto=pasto) # devo creare la consumazione comunque, non può esistere         
    else:
       miodiario = get_object_or_404(Diario,pk=objid)       # se ho fornito l'id, significa che l'oggetto esiste           
       consumazione = miodiario.consumazione_set.filter(tipo_pasto=pasto)[0] # cerco le consumazioni associate, ce n'è sicuramente solo una  
                                   
    mio_alimento = get_object_or_404(Alimento,pk=alimento)                   # cerco l'alimento usando il suo indice che ho ricevuto come parametro
    consumazione.alimento.add(mio_alimento)                                  # lo associo alla sua consumazione
   
    settimana = miodiario.week() 
       
    return HttpResponseRedirect(reverse('diario:modifica',args=(miodiario.id,settimana,strpasto,giorno,)))

@login_required   #per mettere autenticazione inserisco solo il decoratore qui  
def inserisci(request):
# inserisce un nuovo oggetto evento del giorno nel diario nel sistema

    data = request.POST.get('data')
    note = request.POST.get('note')
    
    diario = Diario()
    diario.data = data
    diario.note = note
    diario.save()
    
    return HttpResponseRedirect(reverse('diario:index'))

@login_required
def cancella(request,idGiorno,pasto,al,week,day):
   # riceve i'id della registrazione giornaliera, il numero della consumazione 
   # e il nome alimento. Lo cancella dalla lista della consumazione
    from . import config
    #PASTI = ['fuori_pasto','colazione','merenda_mat','pranzo','merenda_pom',
    #        'cena','dopo_cena']
    reg   = Diario.objects.get(id=idGiorno)       # identifico la registrazione giornaliera
    liscons = reg.consumazione_set.all()          # identifico la consumazione
    plist = liscons.filter(tipo_pasto=pasto)[0]   # filtro rispetto al pasto
    plist.alimento.remove(al)                     # lo elimino dalla lista
    return HttpResponseRedirect(reverse('diario:modifica',args = (idGiorno,week,config.PASTIL[pasto],day))) # reindirizzo a index


def mioLogin(request):
   # manda alla finestra di autenticazione, per chiedere username e password
   next = request.GET['next']
   context = {'next':next,}
   return render(request,'diario/login.html',context)



def autentica(request):
   # riceve dalla finestra di autenticazione e controlla per effettuare il login
   utente  = request.POST.get('utonto') 
   password = request.POST.get('password')
   next = request.POST.get('next')
   user = authenticate(request, username=utente, password=password)
 
   if user is not None:
      login(request, user)
      return HttpResponseRedirect(next)
   else:
      return render(request,'diario/login.html',{'msg':'Autenticazione Fallita', 'next':next} )



