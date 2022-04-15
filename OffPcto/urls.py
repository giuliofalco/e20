from django.urls import path
from . import views

app_name="OffPcto"

urlpatterns = [
      path('',views.index,name="index"),
      path('tutor/',views.tutor,name="tutor"),
      path('aziende/',views.aziende,name="aziende"),
      path('carica_tutor/',views.carica_tutor,name='carica_tutor')
     # path('aziende/',AziendeListView.as_view(),name='AziendeListView'),
]
