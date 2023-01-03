from django.urls import path
from . import views

app_name="contatti"

urlpatterns = [
      path('',views.index,name="index"),
      path('aziende',views.aziende,name="aziende"),
      path('aziende/<str:id>',views.dettaglio_azienda,name="dettaglio_aziende"),
      path('add_contatto',views.add_contatto,name="add_contatto"),
      path('cancella_contatto',views.cancella_contatto,name="cancella_contatto"),
]
