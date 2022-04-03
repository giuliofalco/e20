from django.urls import path
from . import views

app_name="diario"

urlpatterns = [
      path('',views.index,name="index"),
      path('<int:w>',views.settimana,name="settimana"),
      path('modifica/<int:id>/<int:week>/<str:pasto>/<int:day>',views.modifica,name="modifica"),
      path('registra',views.registra,name="registra"),
      path('inserisci',views.inserisci,name="inserisci"),
      path('cancella/<int:idGiorno>/<int:pasto>/<int:al>',views.cancella,name="cancella"),
]
