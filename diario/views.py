from django.shortcuts import render
from django.http import HttpResponse
from diario.models import Diario, Consumazione, Alimento
from django.template import loader
from django.urls import reverse
from . import myDate 

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
   # genero una lista di liste. Ogni componente è una lista il cui primo elemento è il numero della
   # settimana e il secondo è la lista che contiene le registrazioni di quella settimana 
   # e. [[7,[ogg1, ogg2, ogg3]], [11, [ogg4,ogg5]] ogni ogg è un oggetto di Diario
   
   context = {'lista_settimanale': dati}
 
   return render(request, 'diario/index.html', context)

def settimana(request,w):
      PASTI = ['fuori_pasto','colazione',2,'merenda_mat','pranzo','merenda_pom','cena','dopo_cena']
      lista = Diario.objects.all()                        # tutte le registrazioni
      weekly = [obj for obj in lista if obj.week() == w]  # solo quelle della settimana w   
      cons = [[w.week_day,list(w.consumazione_set.all())] for w in weekly]
      # estraggo da weekly (lista degli oggetti Diario di quella particolare settimana)
      # per ogni elemento di weekly le consumazioni ad esso associate. Trasformo il querySet in lista
      # produco una lista il cui elemnti sono il giorno della settimana ('lun', 'mart', seguito 
      # dalla data) e dalla lista delle consumazioni di quel giorno
     
      # per ottenere un report tabellare in cui ogni riga sia una consumazione e le colonne i
      # giorni:
      # preparo un dizionario in cui la chiave, sia il nome di una consumazione
      # e il valore una lista di elementi il cui primo elemento è il weekday, e il secondo
      # la lista degli alimenti della consumazione in quel giorno
      
      PASTI = ['fuori_pasto','colazione','merenda_mat','pranzo','merenda_pom','cena','dopo_cena']
      # inizializzo la struttura: lista con tante righe quanti sono i tipi di pasto
      # ogni righe è una lista, il primo elemento il nome del pasto, il secondo una lista di 7
      # elementi, ciascuno dei quali conterrà gli alimenti consumati in quel giorno e il quel pasto
      struttura = [[PASTI[j], ["" for i in range(7)]] for j in range(len(PASTI))]
      
      # riempio la struttura
      for obj in weekly:
          col = obj.w_day() - 1                    # la colonna è data dal giorno della settimana
          for cons in obj.consumazione_set.all():  # esplodo l'oggetto diario nelle sue consumazioni
              riga = cons.tipo_pasto               # il numero di riga corrisponde al tipo di pasto
              cont = cons.alimento.all()           # esplodo negli alimenti associati a quella consum.
              struttura[riga][1][col] = cont       # colloco gli alimenti nella corretta posizione
      
      # mi serve per intestare le colonne della tabella
      GIORNI = ["lun","mar","mer","gio","ven","sab","dom"] 
     
      
      md = myDate.MyDate()                         
      periodo = md.str_week(w)                     # calcolo data di inizio e fine della settimana w
      
      FRUTTA =  ['pompelmi','fragole']
      context = {'settimana': w,'struttura': struttura, 'pasti':PASTI, 'periodo': periodo, 
                 'altro': FRUTTA, 'giorni': GIORNI}
                  
      return render(request,'diario/settimana.html',context)
      
      
  

