import os
import calendar
from django.shortcuts import render, redirect
from django.conf import settings
from datetime import date, datetime, timedelta
from .models import DayEntry
from .forms import DayEntryForm
from .filters import *
from calendar import monthrange
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import FileResponse
from collections import  defaultdict # ,OrderedDict
from django.http import HttpResponseRedirect
from django.urls import reverse
#from urllib.parse import quote, unquote
from django.contrib.auth import logout
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
import locale

locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')


WEEKDAY = ('Lunedì','Martedì','Mercoledì','Giovedì','Venerdì','Sabato','Domenica')

MESI = ('Gennaio', 'Febbraio', 'Marzo','Aprile',
        'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre',
        'Ottobre', 'Novembre', 'Dicembre')

@login_required
def calendar_view(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))    # per default inizia dalla data odierna
    month = int(request.GET.get('month', today.month))
   
    # Gestisci i limiti dei mesi
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    days_in_month = monthrange(year, month)[1]    # numero di giorni nel mese
    month_name = calendar.month_name[month]       # nome del mese
    first_weekday = date(year, month, 1).weekday() # giorno della settimana del primo del mese
    last_weekday = date(year, month, days_in_month).weekday() # giorno della settimana dell'ultimo del mese
    
    days = [] # colleziono gli oggetti giorno da passare al template
    for day in range(1, days_in_month + 1):
        giorno = {
        "day": day,
        "date": date(year, month, day),
        "is_today": today.year == year and today.month == month and today.day == day,
        }
        print("giorno =",year, month, day) # debug
        try: # se il giorno esiste nel database controllo se è stato aggiornato piu di recente verificando il cookie
            record_giorno = DayEntry.objects.get(date=date(year,month,day),user=request.user)
            cookie = request.COOKIES.get(date(year,month,day).strftime("%Y-%m-%d")+str(request.user))
            updated =   record_giorno.updated_at.strftime("%Y-%m-%d %H:%M")
            print("updated_at=",updated,"cooky=",cookie)
            if record_giorno.vuoto():
                dot = False
            elif cookie:
                dot = updated != cookie
            else:
                dot = True
            giorno['full'] = not record_giorno.vuoto() # controllo che ci sia qualcosa di significativo in uno dei campi
        except DayEntry.DoesNotExist: # se non esiste quel giorno nel database ignoro
            dot = False
            giorno['full']= False # il record è vuoto
        giorno['dot'] = dot
       
        
        days.append(giorno)
   
    # Celle vuote all'inizio e alla fine
    empty_start = list(range(first_weekday))   # Celle vuote prima del primo giorno
    empty_end = list(range(6 - last_weekday))  # Celle vuote dopo l'ultimo giorno
    context = {
        'days': days,
        'year': year,
        'month': month,
        'month_name': month_name,
        'mese': MESI[month-1],
        'first_weekday': first_weekday,  # Giorno della settimana del primo giorno
        'last_weekday': last_weekday,    # Giorno della settimana dell'ultimo giorno
        'empty_start': empty_start,
        'empty_end': empty_end,
    }
    return render(request, 'agenda/calendar_view.html', context)

@login_required
def day_editor(request, year, month, day):
    entry_date = date(year, month, day)
    prev_date = entry_date - timedelta(days=1)
    next_date = entry_date + timedelta(days=1)

    # cerca l'entry solo tra quelle dell'utente
    day_entry = DayEntry.objects.filter(user=request.user, date=entry_date).first()
    created = False
    if not day_entry:
        # se non esiste, la crea assegnando l'utente
        day_entry = DayEntry(user=request.user, date=entry_date)
        day_entry.save()
        created = True

    # day_entry, created = DayEntry.objects.get_or_create(date=entry_date)
    weekday = WEEKDAY[entry_date.weekday()]

    if request.method == 'POST':
        form = DayEntryForm(request.POST, instance=day_entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user  # riassicura che l'utente sia corretto
            entry.save()

            response = HttpResponseRedirect(reverse('agenda:calendar_view'))
            response.set_cookie(
                key=day_entry.date.strftime('%Y-%m-%d'),
                value=day_entry.updated_at.strftime('%Y-%m-%d %H:%M')+str(request.user),
                max_age=60 * 60 * 24 * 365  # Cookie valido per 1 anno
            )
            return response
    else:
        form = DayEntryForm(instance=day_entry)
        # elenco_progetti = Projects.objects.all()

        context = {'form': form, 'entry_date': entry_date, 'mese':MESI[month-1],
                   'prev_day': prev_date.day, 'next_day':next_date.day, 
                   'prev_month':prev_date.month, 'next_month':next_date.month,
                   'prev_year': prev_date.year,'next_year': next_date.year, 
                   'weekday' : weekday, 
                   #'elenco_progetti':elenco_progetti,
        }
        response = render(request, 'agenda/day_editor.html', context )
        response.set_cookie(
                key=day_entry.date.strftime('%Y-%m-%d'),
                value=day_entry.updated_at.strftime('%Y-%m-%d %H:%M')+str(request.user),
                max_age=60 * 60 * 24 * 365  # Cookie valido per 1 anno
        )
       
        return response



@xframe_options_exempt
def serve_pdf(request, filename):
    # view di test per poter incorporare un file pdf in un iframe
    filepath = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)
    response = FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    response['X-Frame-Options'] = 'SAMEORIGIN'
    response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
    return response


def monthly_report(request):
    # view per il report di backup dei dati raggrupapti per mese
    # Ottieni tutti i record con almeno un campo non vuoto

    entries = DayEntry.objects.filter(
        Q(assenze__isnull=False, assenze__gt='') |
        Q(eventi__isnull=False, eventi__gt='') |
        Q(uscite__isnull=False, uscite__gt='') |
        Q(note__isnull=False, note__gt='')
    ).filter(user=request.user)
  
    # Organizza i dati per mese
    data_by_month = {}
    for entry in entries:
        # Ottieni il mese e l'anno come stringa leggibile (es. "Gennaio 2025")
        month = entry.date.strftime('%B %Y').capitalize()
        if month not in data_by_month:
            data_by_month[month] = []
        # Aggiungi il record al mese corrispondente
        data_by_month[month].append({
            'date': entry.date.strftime('%d-%m-%Y'),
            'assenze': entry.assenze,
            'eventi': entry.eventi,
            'uscite': entry.uscite,
            'note': entry.note,
        })
    
    parola = ''
    if request.method == 'POST':             # richiama il filtro
        parola = request.POST.get('q','')
        data_by_month = filtra_dizionario(data_by_month,parola)

     # Ordina i mesi in ordine decrescente
    sorted_months = sorted(data_by_month.keys(), key=lambda month: datetime.strptime(month, "%B %Y"), reverse=True)
     # Crea un nuovo dizionario con i mesi ordinati
    data_by_month = {month: data_by_month[month] for month in sorted_months}
    # Ordina i giorni all'interno di ogni mese
    for month in data_by_month:
        data_by_month[month].sort(key=lambda x: x['date'],reverse=True)
    # Passa i dati al template
    return render(request, 'agenda/monthly_report.html', {'data_by_month': data_by_month, 'parola':parola})

def logout_view(request):
    logout(request)
    return redirect('agenda:calendar_view')

def weekly_report(request):
    # organizza il report per settimana
    # Ottieni tutti i record con almeno un campo non vuoto
    entries = DayEntry.objects.filter(
        Q(assenze__isnull=False, assenze__gt='') |
        Q(eventi__isnull=False, eventi__gt='') |
        Q(uscite__isnull=False, uscite__gt='') |
        Q(note__isnull=False, note__gt='')
    ).filter(user=request.user)

    # Organizza i dati per settimana
    data_by_week = defaultdict(list)
    for entry in entries:
        start_of_week = entry.date - timedelta(days=entry.date.weekday())  # Lunedì
        end_of_week = start_of_week + timedelta(days=6)                    # Domenica
        week_key = (start_of_week, end_of_week)
        data_by_week[week_key].append({
            # 'date': entry.date.strftime('%d-%m-%Y'),
            'date': entry.date.strftime('%d-%m-%Y %A').capitalize(),
            'assenze': entry.assenze,
            'eventi': entry.eventi,
            'uscite': entry.uscite,
            'note': entry.note,
        })

    parola = ''
    if request.method == 'POST':
        parola = request.POST.get('q', '')
        data_by_week = filtra_dizionario(data_by_week, parola)

    # Ordina le settimane in ordine decrescente
    sorted_weeks = sorted(data_by_week.keys(), key=lambda k: k[0], reverse=True)
    data_by_week = {week: data_by_week[week] for week in sorted_weeks}

    # Ordina i giorni all'interno di ogni settimana (opzionale, decrescente)
    for week in data_by_week:
        data_by_week[week].sort(key=lambda x: x['date'])

    return render(request, 'agenda/weekly_report.html', {
        'data_by_week': data_by_week,
        'parola': parola
    })

def redirect_to_day_editor(request, date_str):
    # Converte la stringa della data nel formato "21-04-2025 Lunedi" e rimanda a day_editor del giorno indicato
    try:
        date_obj = datetime.strptime(date_str, '%d-%m-%Y %A')
    except ValueError:
        # Se la data non è nel formato corretto, manda un errore o una risposta personalizzata
        return redirect('agenda:weekly_report')
    
    # Redirige alla view 'day_editor' con i parametri year, month, day
    return redirect('agenda:day_editor', year=date_obj.year, month=date_obj.month, day=date_obj.day)

@login_required
def genera_password(request):
    # genera una passowrd da utilizzare per le registrazioni, 
    # a partire dal nome del servizio ed una parola segreta
    return render(request, 'agenda/genera_password.html')



