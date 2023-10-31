from django.urls import path
from . import views

app_name="contatti"

urlpatterns = [
      path('',views.index,name="index"),
      path('aziende',views.aziende,name="aziende"),
      path('aziende/<str:id>',views.dettaglio_azienda,name="dettaglio_aziende"),
      path('add_contatto',views.add_contatto,name="add_contatto"),
      path('cancella_contatto',views.cancella_contatto,name="cancella_contatto"),
      path('contatti',views.contatti,name="contatti"),
      path('insert',views.insertCompany,name='insert'),
      path('richieste_contatti',views.richieste_contatti,name='richieste_contatti'),
]
