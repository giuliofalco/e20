from datetime import *
class MyDate():
    mesi      = ['gen','feb','mar','apr','mag','giu','lug','ago','set','ott','nov','dic'] # nomi dei mesi
    giorni    = ['lun','mar','mer','gio','ven','sab','dom']   # nomi dei giorni della settimana

    def __init__(self, giorno=1, mese=0, anno=0):
        self.giorno = giorno   # default 1 gennaio dell'anno corrente
        self.mese   = mese     # default gennaio
        if anno == 0:
           self.anno   = self.anno_corrente()               # default anno corrente
        else:
           self.anno = anno
        self.g_mesi = [31,28,31,30,31,30,31,31,30,31,30,31] # giorni dei mesi di un anno non bisestile
        if self.anno_bisestile():
           self.g_mesi[1] = 29  # se anno bisestile allora febbraio ha 29 giorni
        self.G_mesi()           # G_mesi, somma cumulativa dei giorni dei mesi 
        self.iso()              # inzio della settimana ISO dell'anno corrente (giorno in cui è lunedì)  
       
          # aggiorna settimane, i giorni di inizio delle settimane

    def anno_corrente(self):
        # restituisce l'anno corrente
        oggi = date.today()
        return oggi.year

    def iso(self):
        # calcola il giorno di partenza della settimana num. 1 dell'anno
        giorno_iso = self.giorno_settimana(1,0,self.anno)
        
        if giorno_iso <= 4:         # 4 è giovedì il giorno esattamente a metà settimana
           self.iso = 1-giorno_iso  # la settimana è quella che contiene un giovedì
        else:
           self.iso = 9-giorno_iso  # la data di partenza della settimana 1 varia da 29 dic al 4 gennaio
                                    # la settimana 1 inizia sempre di lunedì e  l'anno ISO può avere 53 settimane
    def anno_bisestile(self):
        # ritorna True se l'anno corrente è bisestile, False altrimenti
        return self.anno % 4 == 0 and not self.anno % 100 == 0 or self.anno % 400 == 0

    def delta(self,giorno,mese):
      # restituisce il numero di giorni trascorsi dall'inizio anno alla data (giorno,mese) specificata
      return giorno + self.G_mesi[mese]

    def giorno_settimana(self,giorno,mese,anno):
      # calcola il giorno della settimana di data (giorno,mese,anno) come intero ISO (1 = lunedi, 2 = martedi, .. 7 = domenica)
      iso_map = [6,7,1,2,3,4,5]                 # per mappare il giorno della settimana, con numeri da 1 a 7
      giorni = self.delta(giorno,mese)          # gironi trascorsi dall'inizio anno
      gbis   = anno + (anno-1) // 4 - (anno-1) // 100 + (anno-1) // 400
      wday   = (giorni + gbis) % 7              # 0 = sab 1 = dom ..... 6 = ven
     
      return  iso_map[wday]                     # giorno iso: 1 = lun, 2 = mar, ... 6 = sab, 7 = dom

    def str_wday(self,giorno,mese,anno):
         # ritorna i l giorno della settimana in formato stringa
         return self.giorni[self.giorno_settimana(giorno,mese,anno)-1]

    def G_mesi(self):
       # calcola la somma cumulativa dei giorni del mese: G_mesi
       self.G_mesi = [0]
       somma = 0
       for g in self.g_mesi:
           somma = somma + g
           self.G_mesi.append(somma)
    
    def posizione(self,valore, lista):
      # restituisce la posizione del primo elemento di lista >= valore se esiste altrimenti - 1
      for i in range(len(lista)):
          if lista[i] >= valore:
            return i
      return -1 

    def data_delta(self,g):
      # restituisce (giorno,mese) trascorsi g giorni dall'inizio anno
          p = self.posizione(g,self.G_mesi)
          if p == -1:
             return "errore in data_delta(g): g > 365"
          if p == 0:
             return "errore in data_delta(g): g < 0"
          return (g - self.G_mesi[p-1], p-1)

    def delta_settimana(self,week):
       # restituisce la data di inizio e fine  della settimana week ((giorno,mese),(giorno,mese))
       inizio = self.data_delta((week-1)*7+self.iso)
       fine   = self.data_delta((week-1)*7+self.iso + 7)
       return (inizio, fine)
          

    def str_week(self,week):
         # ritorna giorno e mese di inzio e fine come stringa
         t = self.delta_settimana(week)
         #return "da " + str(t[0][0]) + " " + str(self.mesi[t[0][1]]) + " al " + str(t[1][0]-1) + " " + str(self.mesi[t[1][1]])
         res = "da " + str(t[0][0]) + " " + str(self.mesi[t[0][1]]) + " al " 
         if t[1][0] == "e":         
             res = res + "fine anno"
         else:
             res = res + str(t[1][0]-1) + " " + str(self.mesi[t[1][1]])
         return res
    
    def data_wday(self,week,day):
        return self.data_delta((week-1)*7+self.iso+day)  
