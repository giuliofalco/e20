from diario.models import Diario

def lista_settimanale():
# restituisce la lista degli oggetti del Diario, raggruppata per settimane 
    
    lista = Diario.objects.all()                  # lista di tutti i giorni del Diario

    # costruisco la lista con i numeri delle settimane

    weeks = [giorno.week() for giorno in lista]   # lista con i dati compresi i duplicati
    weeks = list(set(weeks)).sort()               # elimino i duplicati
                                                  # trasformo in lista e metto in ordine crescente 

    # produco la lista organizzata per settimane
    # ogni elmento è il numero della settimana seguita dalla lista con gli oggetti Diario
    # appartenenti a quella settimana. Rimangono già ordinati in ordine cronologico

    dati = [[sett,[oggetto for oggetto in lista if oggetto.week()==sett]] for set in weeks]
    return(dati)
