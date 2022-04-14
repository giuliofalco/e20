from django.shortcuts import render
from OffPcto.models import *

def index(request):
    return render(request,'"OffPcto"/index.html',{})
    
def tutor(request):
     elenco = Tutor.objects.all()
     context = {'object_list':elenco}
     return render(request,"OffPcto/tutor.html",context)

def aziende(request):
    elenco = Aziende.objects.all()
    context = {'object_list': elenco}
    return render(request,"OffPcto/aziende.html",context)
    
